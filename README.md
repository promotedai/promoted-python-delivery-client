# promoted-python-delivery-client

Python client SDK for the Promoted.ai Delivery API

## Features

- Demonstrates and implements the recommended practices and data types for calling Promoted.ai's Delivery API.
- Client-side position assignment and paging when not using results from Delivery API, for example when logging only or as part of an experiment control.

## Creating a PromotedDeliveryClient

We recommend creating a `PromotedDeliveryClient` in a separate file so it can be reused.
It is thread-safe and intended to be used as a singleton, leveraging the well-known Python `requests` library for calling Promoted.ai's services.

### `PromotedClient.java`

```python
client = PromotedDeliveryClient(delivery_endpoint=delivery_endpoint,
                                delivery_api_key=delivery_api_key,
                                delivery_timeout_millis=250,
                                metrics_endpoint=metrics_endpoint,
                                metrics_api_key=metrics_api_key,
                                metrics_timeout_millis=1000)
```

### Client Configuration Parameters

| Name                           | Type                           | Description                                                                                                                                                                                                                                                                                                 |
| ------------------------------ | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `delivery_endpoint`            | str                            | API endpoint for Promoted.ai's Delivery API                                                                                                                                                                                                                                                                 |
| `delivery_api_key`             | str                            | API key used in the `x-api-key` header for Promoted.ai's Delivery API                                                                                                                                                                                                                                       |
| `delivery_timeout_millis`      | int                            | Timeout on the Delivery API call. Defaults to 250.                                                                                                                                                                                                                                                          |
| `metrics_endpoint`             | str                            | API endpoint for Promoted.ai's Metrics API                                                                                                                                                                                                                                                                  |
| `metrics_api_key`              | str                            | API key used in the `x-api-key` header for Promoted.ai's Metrics API                                                                                                                                                                                                                                        |
| `metrics_timeout_millis`       | int                            | Timeout on the Metrics API call. Defaults to 3000.                                                                                                                                                                                                                                                          |
| `warmup`                       | bool                           | Option to warm up the HTTP connection pool at initialization, defaults to False.                                                                                                                                                                                                                            |
| `thread_pool_size`             | int                            | Number of threads to use in a `ThreadPoolExecutor` to make background calls for metrics and shadow traffic, defaults to 5.                                                                                                                                                                                  |
| `apply_treatment_checker`      | func[[CohortMembership], bool] | Optional function called during delivery, accepts an experiment and returns a boolean indicating whether the request should be considered part of the control group (False) or in the treatment arm of an experiment (True). If not set, the default behavior of checking the experiement `arm` is applied. |
| `max_request_insertions`       | int                            | Maximum number of request insertions that will be passed to (and returned from) Delivery API. Defaults to 1000.                                                                                                                                                                                             |
| `shadow_traffic_delivery_rate` | float between 0 and 1          | rate = [0,1] of traffic that gets directed to Delivery API as "shadow traffic". Only applies to cases where Delivery API is not called. Defaults to 0 (no shadow traffic).                                                                                                                                  |
| `blocking_shadow_traffic`      | bool                           | Option to make shadow traffic a blocking (as opposed to background) call to delivery API, defaults to False.                                                                                                                                                                                                |
| `perform_checks` | bool | Performs some validation that request fields are filled properly. These checks take time so this should be turned off once a request is satisfactory. |

## Data Types

### UserInfo

Basic information about the request user.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`user_id` | str | Yes | The platform user id, cleared from Promoted logs.
`anon_user_id` | str | Yes | A different user id (presumably a UUID) disconnected from the platform user id (e.g. an "anonymous user id"), good for working with unauthenticated users or implementing right-to-be-forgotten.
`is_internal_user` | bool | Yes | If this user is a test user or not, defaults to false.

---

### CohortMembership

Useful fields for experimentation during the delivery phase.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`arm` | str | Yes | 'CONTROL' or one of the TREATMENT values ('TREATMENT', 'TREATMENT1', etc.).
`cohort_id` | str | Yes | Name of the cohort (e.g. "LOCAL_HOLDOUT" etc.)

---

### Properties

Properties bag. Can create using a `Dict[str, object]`. Has the JSON structure:

```json
  "struct": {
    "product": {
      "id": "product3",
      "title": "Product 3",
      "url": "www.mymarket.com/p/3"
      // other key-value pairs...
    }
  }
```

---

### Insertion

Content being served at a certain position.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`user_info` | UserInfo | Yes | The user info structure.
`insertion_id` | str | Yes | Generated by the SDK (_do not set_)
`content_id` | str | No | Identifier for the content to be ranked, must be set.
`retrieval_rank` | int | Yes | Optional original ranking of this content item.
`retrieval_score` | float | Yes | Optional original quality score of this content item.
`properties` | Properties | Yes | Any additional custom properties to associate. For v1 integrations, it is fine not to fill in all the properties.

Insertions can be specified in a more compact manner using the request-level  `insertion_matrix_headers` and `insertion_matrix` fields. This can improve latency when there are many insertions or many properties.

For example, instead of defining a request like so:

```python
insertion = [
  Insertion(content_id="28835", properties=Properties(struct={"price": 1.23})),
  Insertion(content_id="37796", properties=Properties(struct={"price": 0})),
  Insertion(content_id="49815"),
]
req = Request(insertion=insertion, ...)
```

It could be defined as:

```python
insertion_matrix_headers = ["contentId", "price"]
insertion_matrix = [
  ["28835", 1.23],
  ["37796", 0],
  ["49815", None],
]
req = Request(insertion_matrix_headers=insertion_matrix_headers,
              insertion_matrix=insertion_matrix,
              ...
)
```

Things to note:
* Properties with nested `struct`s should concatenate paths with a `.` (period).
* Properties which don't exist for an insertion must be specified as `None`.

The `perform_checks` client parameter can help ensure correct usage.

---

### Size

User's screen dimensions.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`width` | int | No | Screen width
`height` | int | No | Screen height

---

### Screen

State of the screen including scaling.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`size` | Size | Yes | Screen size
`scale` | float | Yes | Current screen scaling factor

---

### ClientHints

Alternative to user-agent strings. See https://raw.githubusercontent.com/snowplow/iglu-central/master/schemas/org.ietf/http_client_hints/jsonschema/1-0-0
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`is_mobile` | bool | Yes | Mobile flag
`brand` | ClientBrandHint[] | Yes |
`architecture` | str | Yes |
`model` | str | Yes |
`platform` | str | Yes |
`platform_version` | str | Yes |
`ua_full_version` | str | Yes |

---

### ClientBrandHint

See https://raw.githubusercontent.com/snowplow/iglu-central/master/schemas/org.ietf/http_client_hints/jsonschema/1-0-0
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`brand` | str | Yes | Mobile flag
`version` | str | Yes |

---

### Location

Information about the user's location.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`latitude` | float | No | Location latitude
`longitude` | float | No | Location longitude
`accuracy_in_meters` | int | Yes | Location accuracy if available

---

### Browser

Information about the user's browser.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`user_agent` | str | Yes | Browser user agent string
`viewport_size` | Size | Yes | Size of the browser viewport
`client_hints` | ClientHints | Yes | HTTP client hints structure

---

### Device

Information about the user's device.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`device_type` | one of (`UNKNOWN_DEVICE_TYPE`, `DESKTOP`, `MOBILE`, `TABLET`) | Yes | Type of device
`brand` | str | Yes | "Apple, "google", Samsung", etc.
`manufacturer` | str | Yes | "Apple", "HTC", Motorola", "HUAWEI", etc.
`identifier` | str | Yes | Android: android.os.Build.MODEL; iOS: iPhoneXX,YY, etc.
`screen` | Screen | Yes | Screen dimensions
`ip_address` | str | Yes | Originating IP address
`location` | Location | Yes | Location information
`browser` | Browser | Yes | Browser information

---

### Paging

Describes a page of insertions
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`size` | int | Yes | Size of the page being requested
`offset` | int | Yes | Page offset

---

### Request

A request for content insertions.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`user_info` | UserInfo | Yes | The user info structure.
`requestId` | str | Yes | Generated by the SDK when needed (_do not set_)
`use_case` | str | Yes | One of the use case enum values or strings, i.e. 'FEED', 'SEARCH', etc.
`properties` | Properties | Yes | Any additional custom properties to associate.
`paging` | Paging | Yes | Paging parameters
`device` | Device | Yes | Device information (as available)
`disable_personalization` | bool | Yes | If true, disables personalized inputs into Delivery algorithm.

---

### DeliveryRequest

Input to `deliver`, returns ranked insertions for display.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`request` | Request | No | The underlying request for content, including all candidate insertions with content ids.
`experiment` | CohortMembership | Yes | A cohort to evaluation in experimentation.
`only_log` | bool | Yes | Defaults to false. Set to true to log the request as the CONTROL arm of an experiment, not call Delivery API, but rather deliver paged insertions from the request.
`insertion_start` | int | Yes | Start index in the request insertions in the list of ALL insertions. See [Pages of Request Insertions](#pages-of-request-insertions) for more details.

---

### DeliveryResponse

Output of `deliver`, includes the ranked insertions for you to display.
Field Name | Type | Optional? | Description
---------- | ---- | --------- | -----------
`response` | Response | No | The reponse from Delivery API, which includes the insertions. These are from Delivery API (when `deliver` was called, i.e. we weren't either only-log or part of an experiment) or the input insertions (when the other conditions don't hold).
`client_request_id` | str | Yes | Client-generated request id sent to Delivery API and may be useful for logging and debugging. You may fill this in yourself if you have a suitable id, otherwise the SDK will generate one.
`execution_server` | one of 'API' or 'SDK' | Yes | Indicates if response insertions on a delivery request came from the API or the SDK.

---

### PromotedDeliveryClient

| Method    | Input           | Output           | Description                                                                                           |
| --------- | --------------- | ---------------- | ----------------------------------------------------------------------------------------------------- |
| `deliver` | DeliveryRequest | DeliveryResponse | Makes a request (subject to experimentation) to Delivery API for insertions, which are then returned. |

---

## Calling the Delivery API

Let's say the previous code looks like this:

```python
def get_products(req: ProductRequest):
    products = ...; // Logic to get products from DB, apply filtering, etc.
    sendSuccessToClient(products)
```

We might modify to something like this:

```python
def get_products(req: ProductRequest):
    products = ...; // Logic to get products from DB, apply filtering, etc.

    insertion: List[Insertion] = []

    # Keep a map for reordering
    product_map: Dict[str, Product] = {}

    for product in range(products):
        ins = Insertion(content_id=product.product_id)
        insertion.append(ins)
        product_map[product.product_id] = product

    req = Request(insertion=insertion,
                  user_info=UserInfo(anon_user_id="abc"),
                  paging=Paging(size=100, offset=0))

    delivery_req = DeliveryRequest(request=req)

    resp = client.deliver(delivery_req)

    ranked_products: List[Product] = []
    for ins in range(resp.response.insertion):
        ranked_products.append(product_map[ins.content_id]))

    sendSuccessToClient(ranked_products)
```

## Pages of Request Insertions

Clients can send a subset of all request insertions to Promoted in Delivery API's `request.insertion` array. The `insertion_start` property specifies the start index of the array `request.insertion` in the list of ALL request insertions.

`request.paging.offset` should be set to the zero-based position in ALL request insertions (_not_ the relative position in the `request.insertion` array).

Examples

- If there are 10 items and all 10 items are in `request.insertion`, then insertion_start=0.
- If there are 10,000 items and the first 500 items are on `request.insertion`, then insertionStart=0.
- If there are 10,000 items and we want to send items [500,1000) on `request.insertion`, then insertionStart=500.
- If there are 10,000 items and we want to send the last page [9500,10000) on `request.insertion`, then insertionStart=9500.

`insertion_start` is required to be less than `paging.offset` or else a `ValueError` will result.

Additional details: https://docs.promoted.ai/docs/ranking-requests#sending-even-more-request-insertions

## Logging only

You can use `deliver` but add a `only_log: True` parameter to the `DeliveryRequest`.

### Position

- Do not set the insertion `position` field in client code. The SDK and Delivery API will set it when `deliver` is called.

### Experiments

Promoted supports the ability to run Promoted-side experiments. Sometimes it is useful to run an experiment in your where `promoted-java-delivery-client` is integrated (e.g. you want arm assignments to match your own internal experiment arm assignments).

```python
# Create a small config indicating the experiment is a 50-50 experiment where 10% of the users are activated.
experiment_config = create_50_50_two_arm_experiment_config("promoted-v1", 5, 5)

def get_products(req: ProductRequest):
    products = ...; // Logic to get products from DB, apply filtering, etc.

    # This gets the anonymous user id from the request.
    anon_user_id = get_anon_user_id(req)
    experiment_membership = experimentConfig.check_membership(anon_user_id)

    req = Request(insertion=insertion,
                  user_info=UserInfo(anon_user_id="abc"),
                  paging=Paging(size=100, offset=0))

    # If experimentActivated can be false (e.g. only 5% of users get put into an experiment) and
    # you want the non-activated behavior to not call Delivery API, then you need to specify onlyLog to false.
    # This is common during ramp up.  `onlyLog` can be dropped if it's always false.
    #
    # Example:
    # `onlyLog: experimentMembership is None`
    deliveryRequest = DeliveryRequest(request=req, experiment=experiment_membership)

    response = client.deliver(delivery_request)
    # ...
```

Here's an example using custom arm assignment logic (not using `twoArmExperimentConfig5050`).

```python
    # If you already use an experiment framework, it'll have the ability to return
    # (1) if a user is activated into an experiment and
    # (2) which arm to perform.
    #
    experimentMembership: CohortMembership = None
    if is_user_activated(experimentName, anon_user_id):
        in_treatment = is_user_in_treatment_arm(experiment_name, anon_user_id)

        # Only log if the user is activated into the experiment.
        experiment_membership = CohortMembership(cohort_id=experiment_name,
                                                 arm=(CohortArm.TREATMENT if in_treatment else CohortArm.CONTROL);
```

## SDK Development

### Prereqs

- wheel
- setuptools
- twine
- [bump2version](https://github.com/c4urself/bump2version/)

### Development

- Follow the setup script from the GitHub Action.
- Build wheel: `python setup.py bdist_wheel`
- Install locally: `pip install dist/promoted_python_delivery_client-2.2.0-py3-none-any.whl --force-reinstall`
- Try it out:
  - See the `scripts/` directory.
  - Create a `scripts/.env` file with a few variables:
    ```sh
    DELIVERY_ENDPOINT=<GET ME FROM PROMOTED>
    DELIVERY_API_KEY=<GET ME FROM PROMOTED>
    METRICS_ENDPOINT=<GET ME FROM PROMOTED>
    METRICS_API_KEY=<GET ME FROM PROMOTED>
    ```
  - Invoke (for example) `python3 scripts/call_delivery.py`.

### Testing

#### Unit tests

- Use pytest:
  - `pytest tests/`

### Release

- Create a development branch.  The following command will create a commit with the version update.
- `bump2version [major|minor|patch]`.  These are the strings (e.g. `major`).  This is not the version number.
- Send a pull request and merge.
- Clear dist: `rm -rf dist/`
- Build wheel: `python setup.py bdist_wheel`
- `python3 -m twine upload dist/*`
  - [PyPi](https://pypi.org/project/promoted-python-delivery-client/)
  - You should use an account with MFA setup.  Follow the API token UI for the username and password.  Username is `__token__`.  Password is the API key from the UI.
  - FUTURE: Do this with a Github Action.

### Dependencies

- [dataclasses-json](https://github.com/lidatong/dataclasses-json) -- flexible JSON serialization and deserialization of Python dataclasses. One key feature we use is the ability to omit None's (nulls) from request JSON to decrease payload size.
- requests -- defacto standard HTTP library used to call Promoted APIs.
