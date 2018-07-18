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
from typing import Dict, Tuple, List
from datetime import datetime, timedelta
from djmoney.money import Money

from django.conf import settings
from django.contrib.gis import geos
import googlemaps

from . import LookupError
from .models import Courier

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
    time_slots = [
        (t_start.strftime('%-I:%M %p'), t_end.strftime('%-I:%M %p'))
        for t_start, t_end in time_slots
    ]
    return time_slots


def get_delivery_schedule():
    """
    Returns 3-day delivery schedule.
    Offdays, in this case, Sunday is removed from the schedule.
    """
    # TODO(yao): remove past pick up times from today's schedule
    day1, adjusted = adjust_offdays(datetime.now())
    day1_weekday = day1.strftime('%a') if adjusted else 'Today'

    day2, adjusted = adjust_offdays(day1 + timedelta(days=1))
    day2_weekday = day2.strftime('%a') if adjusted else 'Tomorrow'

    day3, _ = adjust_offdays(day2 + timedelta(days=1))
    day3_weekday = day3.strftime('%a')

    schedule = {
        day1_weekday: {
            day1.day: format_time_slots(get_time_slots())
        },
        day2_weekday: {
            day2.day: format_time_slots(get_time_slots())
        },
        day3_weekday: {
            day3.day: format_time_slots(get_time_slots())
        }
    }
    return {'slots': schedule}


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


def get_delivery_quote(pickup: str, dropoffs: [str]):
    """
    Returns a delivery quote.

    The `eta` is the estimated time of arrival at the origin address.
    The `pricing` is the delivery fee.
    """
    # TODO(yao): handle timeout
    # TODO(yao): factor in package size & type
    # TODO(yao): multi drops
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


def breakdown_fees(quote):
    # Sendhut commission
    # Cost of goods sold
    # Cost of payment processing
    # Contributing margin
    pass
