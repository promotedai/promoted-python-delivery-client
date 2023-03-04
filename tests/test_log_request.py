
import json
from promoted_python_delivery_client.model.delivery_execution import DeliveryExecution
from promoted_python_delivery_client.model.delivery_log import DeliveryLog
from promoted_python_delivery_client.model.execution_server import ExecutionServer
from promoted_python_delivery_client.model.log_request import LogRequest
from promoted_python_delivery_client.model.request import Request
from promoted_python_delivery_client.model.response import Response
from promoted_python_delivery_client.client.serde import log_request_to_json_3


def test_to_json():
    exec = DeliveryExecution(execution_server=ExecutionServer.API, server_version="python.1.1.1")
    dl = DeliveryLog(Request(insertion=[]), Response(request_id='', insertion=[]), exec)
    log_req = LogRequest(delivery_log=[dl])

    data_str = log_request_to_json_3(log_req)
    data = json.loads(data_str)

    # ExecutionServer should be the number, not the name.
    assert data["deliveryLog"][0]["execution"]["executionServer"] == 1
