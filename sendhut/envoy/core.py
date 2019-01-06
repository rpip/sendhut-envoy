"""
# The dispatch algorithm:
Dispatch to nearest available rider within a certain dispatch radius.
Stays on phone for 7 seconds. If order is not picked, dispatch to the next
nearest available rider if not picked for the same amount of time.
Repeats to all riders within that radius until the order is confirmed.

# Food pickups
For food orders, charge a convenience fee in addition to the delivery fee.
It's a flat fee and amounts to x% of the order. It factors things
like delivery distance and size of order.

Also factor in food preparation time (confirm with restaurants).

A variable percentage-based service fee is also applied to the price
of the items that are ordered.

# ETAs
- distance between nearest available envoy and pickup point
- if nearest available is on-task, also factor the estimated
  completion time for current task
"""
import logging
from typing import Dict, Tuple, List
from datetime import datetime, timedelta
from djmoney.money import Money

from django.conf import settings
from django.contrib.gis import geos
import googlemaps

from . import LookupError, LOCATIONS, DELIVERY_TYPE
from .models import (
    Address,
    Contact,
    Pickup,
    Dropoff,
    Courier,
    Delivery,
    Batch
)

logger = logging.getLogger(__name__)

# geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

BASE_FARE = 300
FEE_PER_MILE = 65
TOLL_FEE = 100

KM_TO_MILES_FACTOR = 0.621371

# mo work on sunday, weekday 6
SUNDAY = 6


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def get_time_slots(start=None, end=None, gap=14, delta=30):
    start = start or datetime.today().replace(hour=9, minute=delta)
    end = end or (start + timedelta(hours=gap))
    slots = list(datetime_range(start, end, timedelta(minutes=delta)))
    return zip(slots[:13], slots[1:])


def adjust_offdays(date):
    if date.weekday() == SUNDAY:
        return (date + timedelta(days=1)), True
    return date, False


def format_time_slots(time_slots):
    time_slots = (
        {
            "start_time": t_start,
            "end_time": t_end
        }
        for t_start, t_end in time_slots
    )
    return time_slots


def zone_info(zone):
    return {
        "region": "swa", # southern west africa
        "name": zone,
        "code": zone,
        "timezone": "Africa/Accra",
        "latitude": 51.528642,
        "longitude": -0.101599
    }


def get_scheduling_slots(
        city=LOCATIONS.ACCRA,
        type=DELIVERY_TYPE.PICKUP, date=None):
    """
    Returns 3-day delivery schedule.
    Offdays, in this case, Sunday is removed from the schedule.
    """
    # TODO(yao): remove past pick up times from today's schedule
    day1, adjusted = adjust_offdays(
        datetime.today().replace(hour=9, minute=30, second=0, microsecond=0)
    )
    day1_weekday = day1.strftime('%a') if adjusted else 'Today'

    day2, adjusted = adjust_offdays(day1 + timedelta(days=1))
    day2_weekday = day2.strftime('%a') if adjusted else 'Tomorrow'

    day3, _ = adjust_offdays(day2 + timedelta(days=1))
    day3_weekday = day3.strftime('%a')

    schedule = [
        {'day_name': day1_weekday,
         'day_num': day1.day,
         'slots': format_time_slots(get_time_slots())
         },
        {'day_name': day2_weekday,
         'day_num': day2.day,
         'slots': format_time_slots(get_time_slots(day2))
         },
        {'day_name': day3_weekday,
         'day_num': day3.day,
         'slots': format_time_slots(get_time_slots(day3))
         },
    ]
    return {
        'zone': zone_info(city),
        'type': type,
        'date': date or datetime.now(),
        'schedule': schedule
    }


def calculate_pricing(distance):
    """
    Calculates delivery fee.

    Trip fares start with a base amount, then increase with time and distance.

    - pricing brackets: below 1.5 Miles, 1.5 - 2.5 Miles,  2.5 - 5 Miles, Above 5 Miles
    - base fare of 300 NGN (a flat fee that covers the pickup price)
    - then increase with time and distance, 65NGN/KM

    # TODO
    - dynamic pricing:
      - Traffic, events, weather, timings and driver expertise
      - Distane. The distance between the pickup point and delivery point.
      - Location specific factors such as toll gate fees
      - Demand. This may mean price surge at peak times
      - Vehicle type
      - Batched delivery or one-off
      - size of the package
      - multidrop: Pricing is based on distance, from pickup to drop off,
    driving down the price per drop.
    """
    # TODO(yao): check number of Toll fees to pay
    return (distance * FEE_PER_MILE) + BASE_FARE + TOLL_FEE


def get_delivery_quotev1(pickup: str, dropoffs: [str]):
    """
    Returns a delivery quote for single dropoffs. quick estimates

    The `eta` is the estimated time of arrival at the origin address.
    The `pricing` is the delivery fee.
    """
    # TODO(yao): handle timeout
    # TODO(yao): factor in package size & type
    dropoff = dropoffs[0]
    resp = gmaps.distance_matrix(
        origins=pickup, destinations=dropoff, units='imperial')
    resp = resp['rows'][0]['elements'][0]
    if resp['status'] != 'OK':
        raise LookupError(status=resp['status'])

    distance = (resp['distance']['value']/1000) * KM_TO_MILES_FACTOR
    pricing = calculate_pricing(distance)
    return {
        'pricing': str(Money(pricing, settings.DEFAULT_CURRENCY)),
        'eta': resp['duration']['text']
    }


def get_delivery_quote(pickup: dict, dropoffs: [dict]):
    """
    Returns a delivery quote

    The `eta` is the estimated time of arrival at the origin address.
    The `pricing` is the delivery fee.
    """
    # TODO(yao): handle timeout
    # TODO(yao): factor in package size & type
    pickup = pickup['address']['address']
    dropoffs = [x['address']['address'] for x in dropoffs]
    resp = gmaps.distance_matrix(
        origins=pickup, destinations=dropoffs, units='imperial')
    all_resp = resp['rows'][0]['elements']
    # if resp['status'] != 'OK':
    #     raise LookupError(status=resp['status'])
    pricing = sum([
        calculate_pricing(distance_to_miles(x['distance']['value']))
        for x in all_resp
    ])
    # TODO: make more human friendly
    total_dropoff_time = sum([x['duration']['value'] for x in all_resp])/60
    return {
        'pricing': str(Money(pricing, settings.DEFAULT_CURRENCY)),
        'eta': total_dropoff_time,
        'pricing_int': pricing
    }


def distance_to_miles(val):
    return (val/1000) * KM_TO_MILES_FACTOR


def breakdown_fees(quote):
    # Sendhut commission
    # Cost of goods sold
    # Cost of payment processing
    # Contributing margin
    pass


def create_delivery(user, pickup, dropoffs, quote=None, payment=None):
    # TODO: pay from wallet
    apt = pickup['address'].get('apt')
    addr = Address.objects.create(address=pickup['address'], apt=apt)
    pickup_contact = pickup.get('contact', user.contact_details)
    contact = Contact.objects.create(**pickup_contact)
    pickup = Pickup.objects.create(address=addr, contact=contact)
    batch = Batch.objects.create()
    for d in dropoffs:
        _addr = Address.objects.create(address=d['address'])
        _contact = Contact.objects.create(**d['contact'])
        meta = {'size': d['size'], 'notes': d.get('notes')}
        dropoff = Dropoff.objects.create(
            address=_addr, contact=_contact, metadata=meta)
        delivery = Delivery.objects.create(
            user=user, pickup=pickup, dropoff=dropoff)
        if quote:
            delivery.quote_id = quote

        batch.deliveries.add(delivery)
        batch.record_payment(**payment)

    return batch
