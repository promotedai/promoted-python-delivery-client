import os
from os.path import dirname, abspath
from promoted_python_delivery_client.client.client import PromotedDeliveryClient
from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.model.insertion import Insertion
from promoted_python_delivery_client.model.request import Request
from promoted_python_delivery_client.model.user_info import UserInfo
from dotenv import load_dotenv

path = dirname(abspath(__file__)) + '/.env'
load_dotenv(path)

delivery_endpoint = str(os.getenv("DELIVERY_ENDPOINT"))
delivery_api_key = str(os.getenv("DELIVERY_API_KEY"))
metrics_endpoint = str(os.getenv("METRICS_ENDPOINT"))
metrics_api_key = str(os.getenv("METRICS_API_KEY"))

client = PromotedDeliveryClient(delivery_endpoint=delivery_endpoint,
                                delivery_api_key=delivery_api_key,
                                delivery_timeout_millis=60*1000,
                                metrics_endpoint=metrics_endpoint,
                                metrics_api_key=metrics_api_key,
                                only_log_metrics_request=True)

insertion = [
  Insertion(content_id="28835"),
  Insertion(content_id="57076"),
  Insertion(content_id="37796"),
  Insertion(content_id="52502"),
  Insertion(content_id="49815"),
  Insertion(content_id="26926"),
  Insertion(content_id="51127"),
  Insertion(content_id="14368"),
]
req = Request(insertion=insertion, user_info=UserInfo(log_user_id="abc"))
request = DeliveryRequest(request=req)
print(f"DELIVERY REQUEST: {request.request.to_json()}")  # type: ignore

print()

resp = client.deliver(request)
print(f"DELIVERY RESPONSE: {resp.response.to_json()}")  # type: ignore

client.executor.shutdown()
