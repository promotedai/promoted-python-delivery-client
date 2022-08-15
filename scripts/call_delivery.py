import logging
import os
from os.path import dirname, abspath
import sys
from promoted_python_delivery_client.client.client import PromotedDeliveryClient
from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.model.insertion import Insertion
from promoted_python_delivery_client.model.properties import Properties
from promoted_python_delivery_client.model.request import Request
from promoted_python_delivery_client.model.user_info import UserInfo
from promoted_python_delivery_client.client.serde import delivery_request_to_json_3
from dotenv import load_dotenv

path = dirname(abspath(__file__)) + '/.env'
load_dotenv(path)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

delivery_endpoint = str(os.getenv("DELIVERY_ENDPOINT"))
delivery_api_key = str(os.getenv("DELIVERY_API_KEY"))
metrics_endpoint = str(os.getenv("METRICS_ENDPOINT"))
metrics_api_key = str(os.getenv("METRICS_API_KEY"))

client = PromotedDeliveryClient(delivery_endpoint=delivery_endpoint,
                                delivery_api_key=delivery_api_key,
                                delivery_timeout_millis=60*1000,
                                metrics_endpoint=metrics_endpoint,
                                metrics_api_key=metrics_api_key,
                                only_send_metrics_request_to_logger=True)

insertion = [
  Insertion(content_id="28835", properties=Properties(struct={"price": 1.23})),
  Insertion(content_id="57076", properties=Properties(struct={"price": "4.56"})),
  Insertion(content_id="37796", properties=Properties(struct={"price": 0})),
  Insertion(content_id="52502", properties=Properties(struct={"price": None})),
  Insertion(content_id="49815"),
  Insertion(content_id="26926"),
  Insertion(content_id="51127"),
  Insertion(content_id="14368"),
]
req = Request(insertion=insertion, user_info=UserInfo(log_user_id="abc"))
request = DeliveryRequest(request=req)
print(f"DELIVERY REQUEST: {delivery_request_to_json_3(request.request)}")  # type: ignore

print()

resp = client.deliver(request)
print(f"DELIVERY RESPONSE: {resp.response.to_json()}")  # type: ignore

print()

client.shutdown()
