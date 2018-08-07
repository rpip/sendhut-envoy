FORMAT: 1A
HOST: http://sendhut.apiblueprint.org/

# Sendhut

The API is designed to allow application developers to check prices,
schedules, book a delivery and track a delivery status in real-time.

Our API is REST-based.

* It make use of standard HTTP verbs like GET, POST, PUT and DELETE.
* It uses HTTP response codes to indicate API errors.
* Authentication to the API is performed via HTTP Basic Auth.
* POST data must be sent as JSON.
* All responses are in JSON.

The base URL for all requests to the Sendhut API is: `https://sendhut.com/api`

## Authentication

The Sendhut API requires authentication by HTTP Basic Auth headers.
Your API key should be included as the username. The password is not required.

`Basic Y2YyZjJkNmQtYTMxNC00NGE4LWI2MDAtNTA1M2MwYWYzMTY1Og==`

For Sendhut's internal applications, use the HTTP Basic Auth in combination with the JWT tokens.
To start sending authenticated HTTP requests on behalf of logged in users, you need to
authenticate the user by providng the username and password, and receive a JWT token in return.
Once you have a valid access JWT token you need to add it as a HTTP header to every HTTP request you send to the Sendhut API.
Use the ``

## Metadata:

Updateable objects such as Contact, Delivery have a metadata parameter. You can use this parameter to attach key-value data to these objects.
Metadata is useful for storing additional, structured information on an object.

## Pagination

To paginate list data, use the `page` and `per_page` parameters. By default, list API endpoints
returns 50 items, starting from the first page.

These list API methods share a common structure, taking at least these three parameters: limit, starting_after, and ending_before.

## Responses

The API uses HTTP status codes to indicate the status of your requests.

Status Codes

* 200 - OK: Everything went as planned.
* 400 - Bad Request: often due to missing a required parameter
* 401 - Unauthorized: missing API key or invalid API key provided.
* 402 - Request Failed: The parameters were valid but the request failed.
* 404 - Not Found
* 429 - Too Many Requests
* 500 - Internal Server Error: Something went wrong on Sendhut's end.
* 503 - Service Unavailable: Try again later.


## Errors

Error responses include details about what went wrong. The response format is described as follows:

```json
{
"kind": "error",
"code": "invalid_params",
"message": "The parameters of your request were invalid.",
"details": {
  "dropoff_name": "Dropoff name is required.",
  "dropoff_phone_number": "Dropoff phone number must be valid phone number."
 }
}
```

Please find below the list of all errors:

* invalid_params - The indicated parameters were missing or invalid.
* unknown_location - We weren't able to understand the provided address. This usually indicates the address is wrong, or perhaps not exact enough.
* customer_not_approved - You account has not been approved to create deliveries. Please refer to our approval guidelines for more information.
* account_suspended
* not_found
* service_unavailable
* delivery_limit_exceeded - You have hit the maximum amount of ongoing deliveries allowed.
* couriers_busy - All of our couriers are currently busy.
* out_of_range. This location is out of range

## Delivery status

Deliveries will go through several status transitions until the Job ends:

`pending -> pickup -> dropoff -> delivered`.

Here is a list of all the status transitions:

* pending - We've accepted the delivery and will be assigning it to a courier.
* pickup - Courier is assigned and is en route to pick up the items.
* almost_pickup - The driver is close to the pickup point.
* waiting_at_pickup - The driver is waiting at the pickup point.
* pickup_complete - Courier has picked up the items.
* dropoff - Courier is moving towards the dropoff.
* almost_dropoff - The driver is close to the delivery point.
* waiting_at_dropoff - The driver is waiting at the delivery point.
* canceled - Items won't be delivered. Deliveries are either canceled by the customer or by our customer service team.
* delivered - The package has been delivered successfully.
* returned - The delivery was returned either:
   - customer/sendhut cancelled
   - recipient unavailable
   - recipient asks to reschedule
* scheduled. The job has been scheduled. It will start later.
* expired. Job has expired. No driver accepted the job. It didn't cost any money.

## Returns

If a customer is not available at dropoff, we'll either create a
return delivery or leave items at the door, depending on your preference.

# Data Structures
## `contact` (object)

- `firstname`: `Dany` (string)
- `lastname`: `Dan` (string)
- `phone`: `+33611112222` (string)
- `email`: `client1@email.com` (string)
- `company`: `Sample Company Inc.` (string)

## `pickup` (object)

- `address`: `12 rue rivoli, 75001 Paris` (string)
- `notes`: `Ask Bobby` (string)
- `pickup_time`: `asap` (string)
- `contact` (contact)

## `address` (object)

- `address`: `42 rue rivoli, 75001 Paris` (string)
- `lat`: `87.4` (number)
- `lng`: `98.2` (number)
- `images` (array[string])

## `dropoff` (object)

- `package_type`: `small` (string)
- `package_description`: `The blue one.` (string)
- `address` (address)
- `notes`: `2nd floor on the left` (string)
- `contact` (contact)
- `dropoff_identifier` (contact)

## `cancellation` (object)

- `canceled_by` (object)
- `reason` (object)
- `comment` (object)

## `eta` (object)

- `pickup`: `2017-12-06T16:23:57.000+01:00` (string)
- `dropoff`: `2017-12-06T16:23:57.000+01:00` (string)

## `proof` (object)

- `signature_url`: `https://stuart-bucket.s3.eu-central-1.amazonaws.com/uploads/signatures/d-1618575-d1954390a6.jpg` (string)

## `next` (object)

- `type`: `return` (string)
- `id`: `del_87yjp` (string)

## `delivery` (object)

- `id`: `72251` (number)
- `status`: `delivered` (string)
- `picked_at`: `2017-12-06T16:23:57.000+01:00` (string)
- `delivered_at`: `2017-12-06T16:23:57.000+01:00` (string)
- `tracking_url`: `https://stuart.sandbox.followmy.delivery/72251/3d9e97e10981cffee7777bf0c1d25ad7` (string)
- `package_description`: `The blue one.` (string)
- `package_type`: `small` (string)
- `pickup` (pickup)
- `dropoff` (dropoff)
- `cancellation` (cancellation)
- `eta` (eta)
- `proof` (proof)
- `next` (next)

## `courier` (object)

- `id`: `23129` (number)
- `display_name`: `Sebastien F.` (string)
- `phone`: `+33981270162` (string)
- `picture_url`: `https://stuart.imgix.net/driver/23129/ba04b0d9179f33696367.png` (string)
- `transport_type`: `bike` (string)
- `latitude`: `48.831` (number)
- `longitude`: `2.389` (number)

## `pricing` (object)

- `fee`: `800` (number)
- `currency`: `ngn` (string)
- `invoice_url`: `sendhut.com/invoice` (string)

## `metadata` (object)

## `zone` (object)

- `id`: `2` (number)
- `region`: `swa` (string)
- `name`: `Lagos` (string)
- `code`: `lagos` (string)
- `timezone`: `Africa/Lagos` (string)
- `latitude`: `51.5286416` (number)
- `longitude`: `-0.1015987` (number)

## `slot` (object)

- `start_time`: `2017-07-20T08:45:00.000+01:00` (string)
- `end_time`: `2017-07-20T09:00:00.000+01:00` (string)

## `DeliverySchedule` (object)

- `date`: `2017-07-20T00:00:00.000+01:00` (string)
- `zone` (zone)
- `type`: `pickup` (string)
- `slots` (array[slot])

## `DeliveryQuote` (object)

- `object`: `delivery_quote` (string)
- `id`: `dqt_qUdje83jhdk` (string)
- `created`: `2014-08-26T10:04:03Z` (string)
- `expires`: `2014-08-26T10:09:03Z` (string)
- `fee`: `800` (number)
- `currency`: `ngn` (string)
- `eta`: `2014-08-26T12:15:03Z` (string)
- `duration`: `60` (number)

## DeliveryStatus (enum[string])
+ pick up
+ almost_pickup
+ waiting_at_pickup
+ pickup_complete
+ dropoff
+ almost_dropoff
+ waiting_at_dropoff
+ cancelled
+ delivered
+ returned
+ scheduled
+ expired

## `Delivery` (object)

- `id`: `74853` (number)
- `created_at`: `2017-12-06T16:22:51.000+01:00` (string)
- `status`: `finished` (enum[DeliveryStatus])
- `package_type`: `small` (string)
- `transport_type`: `bike` (string)
- `ended_at`: `2017-12-06T16:23:57.000+01:00` (string)
- `notes`: `Call me when you get to the gate` (string)
- `distance`: `0.348` (number)
- `duration`: `1` (number)
- `quote_id`: `dqt_qUdje83jhdk` (string)
- `deliveries` (array[delivery])
- `courier` (courier)
- `pricing` (pricing)
- `metadata` (metadata)

## `Shipment` (object)

- `pickup` (pickup)
- `dropoffs` (array[dropoff])

## Accounts [/accounts]

## Shipments [/shipments]

Shipment: collection of deliveries which has to be delivered if route is same.

## Get Delivery zones [GET /zones]

This endpoint returns the various active delivery zones within each city.
By default it will return you the picking zone coverage for the cities we operate in.
If you add the type parameter to "delivering" it will return the delivering zone coverage instead.

Coordinates will be in the format [longitude, latitude].

The returned JSON body is a GeoJSON `FeatureCollection objects`.  Read more about the standard here: http://geojson.org/.

To check if an address is within a given zone, use the Delivery Quote endpoint.

+ Response 200 (application/json)

        {
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "properties": {},
              "geometry": {
                "type": "Polygon",
                "coordinates": [
                  [
                    [
                      3.4253311157226562,
                      6.46508076694658
                    ],
                    [
                      3.3882522583007812,
                      6.465251336642291
                    ],
                    [
                      3.3793258666992183,
                      6.457063926366799
                    ],
                    [
                      3.401470184326172,
                      6.443759102328136
                    ],
                    [
                      3.4038734436035156,
                      6.402648405963896
                    ],
                    [
                      3.4263610839843746,
                      6.409471987740317
                    ],
                    [
                      3.4366607666015625,
                      6.42687170785518
                    ],
                    [
                      3.4806060791015625,
                      6.426701125250234
                    ],
                    [
                      3.492622375488281,
                      6.447511780367015
                    ],
                    [
                      3.4757995605468746,
                      6.458428503945924
                    ],
                    [
                      3.4570884704589844,
                      6.465251336642291
                    ],
                    [
                      3.4253311157226562,
                      6.46508076694658
                    ]
                  ]
                ]
              }
            }
          ]
        }


### Get scheduling slots [GET /schedules/{city}/{type}/{date}]

Use this endpoint returns the available schedule slots. Please note the schedules may differ from one city to another.


+ Response 200 (application/json)

    + Attributes (DeliverySchedule)

# Delivery [/deliveries]

Delivery: individual delivery

### Get a Delivery Quote [POST /quotes]

The `eta` is the estimated time of arrival at the origin address
for a given Job by using exactly the same request body as Create a Delivery endpoint.

+ Request

    + Attributes (Shipment)

+ Response 200 (application/json)

    + Attributes (DeliveryQuote)

### List Deliveries [GET]

List all deliveries for a customer.

You can filter the delivery job statuses by using the `status` parameter. See delivery status section above.

+ Response 200 (application/json)

    + Attributes (array[Delivery])

### Create a Delivery [POST]

+ Request

    + Attributes (Shipment)

+ Response 200 (application/json)

    + Attributes (Delivery)

### Get a Delivery [GET /deliveries/{delivery_id}]


+ Response 200 (application/json)

    + Attributes (Delivery)


### Update a Delivery [PATCH /deliveries/{delivery_id}]

You can update several deliveries at the same time, depending on the delivery state.

When the delivery status is `pending`, `picking`, `almost_picking`, `waiting_at_pickup` you can update:

* notes
* package_description
* pickup.comment
* pickup.contact.firstname
* pickup.contact.lastname
* pickup.contact.phone
* pickup.contact.email
* pickup.contact.company
* dropoff.notes
* dropoff.contact.firstname
* dropoff.contact.lastname
* dropoff.contact.phone
* dropoff.contact.email
* dropoff.contact.company

When the delivery status is `dropoff`, `almost_dropoff`, `waiting_at_dropoff` you can update:

* dropoff.notes
* dropoff.contact.firstname
* dropoff.contact.lastname
* dropoff.contact.phone
* dropoff.contact.email
* dropoff.contact.company

+ Response 200 (application/json)

    + Attributes (Delivery)


### Cancel a Delivery [POST /{delivery_id}/cancel]

Cancel an ongoing delivery. A delivery can only be canceled prior to a courier completing pickup.
Delivery fees still apply.

Returns a Delivery object (the new return delivery).

+ Response 200 (application/json)

    + Attributes (Delivery)
