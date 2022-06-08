import logging
import jsonpickle
from typing import Optional
import requests
from promoted_python_delivery_client.model.log_request import LogRequest


# Default timeout for metrics calls.
DEFAULT_METRICS_TIMEOUT_MILLIS = 3000


class APIMetrics:
    def __init__(self,
                 endpoint: str,
                 api_key: str,
                 timeout: Optional[int]) -> None:
        self.endpoint = endpoint
        self.headers = {"x-api-key": api_key}
        self.timeout_in_seconds = timeout / 1000 if timeout is not None else DEFAULT_METRICS_TIMEOUT_MILLIS / 1000

    def run_metrics_logging(self, log_request: LogRequest) -> None:
        payload = jsonpickle.encode(log_request, unpicklable=False)
        r = requests.post(url=self.endpoint,
                          data=payload,
                          timeout=self.timeout_in_seconds,
                          headers=self.headers)
        if r.status_code != 200:
            logging.error(f"Error calling metrics API {r.status_code}")
            raise requests.HTTPError("error calling metrics API")
