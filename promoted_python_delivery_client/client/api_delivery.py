import logging
from typing import Optional
import requests
from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.model.response import Response


# Default timeout for delivery calls.
DEFAULT_DELIVERY_TIMEOUT_MILLIS = 250


class APIDelivery:
    def __init__(self,
                 endpoint: str,
                 api_key: str,
                 timeout: Optional[int]) -> None:
        self.endpoint = endpoint
        self.headers = {"x-api-key": api_key}
        self.timeout_in_seconds = timeout / 1000 if timeout is not None else DEFAULT_DELIVERY_TIMEOUT_MILLIS / 1000

    def run_delivery(self, delivery_request: DeliveryRequest) -> Response:
        request = delivery_request.request
        payload = request.to_json()  # type: ignore this is from dataclass_json
        r = requests.post(url=self.endpoint,
                          data=payload,
                          timeout=self.timeout_in_seconds,
                          headers=self.headers)
        if r.status_code != 200:
            logging.error(f"Error calling delivery API {r.status_code}")
            raise requests.HTTPError("error calling delivery API")
        return Response.from_json(r.content)  # type: ignore this is from dataclass_json
