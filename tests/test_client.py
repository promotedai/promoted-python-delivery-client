from pytest_mock.plugin import MockerFixture
from promoted_python_delivery_client.client.client import PromotedDeliveryClient
from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.model.cohort_arm import CohortArm
from promoted_python_delivery_client.model.cohort_membership import CohortMembership
from promoted_python_delivery_client.model.execution_server import ExecutionServer
from promoted_python_delivery_client.model.log_request import LogRequest
from promoted_python_delivery_client.model.request import Request
from promoted_python_delivery_client.model.response import Response
from tests.dummy_executor import DummyExecutor
from tests.utils_testing import create_test_request_insertions


def test_perform_checks_false_does_not_call_validator(mocker: MockerFixture):
    validate_patch = mocker.patch("promoted_python_delivery_client.client.delivery_request_validator.DeliveryRequestValidator.validate")

    client = create_default_client()
    assert not client.perform_checks  # default false

    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(request=req, only_log=True)

    resp = client.deliver(dreq)
    assert resp is not None
    validate_patch.assert_not_called()


def test_perform_checks_true_does_call_validator_no_shadow_traffic(mocker: MockerFixture):
    validate_patch = mocker.patch("promoted_python_delivery_client.client.delivery_request_validator.DeliveryRequestValidator.validate")

    client = create_default_client()
    assert not client.perform_checks  # default false
    client.perform_checks = True

    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(request=req, only_log=True)

    resp = client.deliver(dreq)
    assert resp is not None
    validate_patch.assert_called_once()
    validate_patch.assert_called_with(dreq, False)


def test_perform_checks_true_does_call_validator_with_shadow_traffic(mocker: MockerFixture):
    validate_patch = mocker.patch("promoted_python_delivery_client.client.delivery_request_validator.DeliveryRequestValidator.validate")

    client = create_default_client()
    assert not client.perform_checks  # default false
    client.perform_checks = True
    client.shadow_traffic_delivery_rate = 1

    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(request=req, only_log=True)

    resp = client.deliver(dreq)
    assert resp is not None
    validate_patch.assert_called_once()
    validate_patch.assert_called_with(dreq, True)


def test_only_log_calls_sdk_delivery_and_logs(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")

    client = create_default_client()

    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(request=req, only_log=True)

    sdk_patch.return_value = Response(insertion=req.insertion)

    resp = client.deliver(dreq)
    assert resp is not None
    assert req.client_request_id
    assert len(resp.response.insertion) == 10
    assert resp.execution_server == ExecutionServer.SDK

    sdk_patch.assert_called_once()
    metrics_patch.assert_called_once()
    api_patch.assert_not_called()

    assert_sdk_log_request(req, resp.response, metrics_patch.call_args[0][0])


def test_custom_not_should_apply_treatment_calls_sdk_delivery_and_logs(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")

    client = create_default_client()
    client.apply_treatment_checker = lambda _: False

    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(request=req, only_log=False)

    sdk_patch.return_value = Response(insertion=req.insertion)

    resp = client.deliver(dreq)
    assert resp is not None
    assert req.client_request_id
    assert len(resp.response.insertion) == 10
    assert resp.execution_server == ExecutionServer.SDK

    sdk_patch.assert_called_once()
    metrics_patch.assert_called_once()
    api_patch.assert_not_called()

    assert_sdk_log_request(req, resp.response, metrics_patch.call_args[0][0])


def test_custom_should_apply_treatment_calls_api_delivery_and_does_not_log(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")

    client = create_default_client()
    client.apply_treatment_checker = lambda _: True

    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(request=req, only_log=False)

    api_patch.return_value = Response(insertion=req.insertion)

    resp = client.deliver(dreq)
    assert resp is not None
    assert req.client_request_id
    assert len(resp.response.insertion) == 10
    assert resp.execution_server == ExecutionServer.API

    sdk_patch.assert_not_called()
    metrics_patch.assert_not_called()
    api_patch.assert_called_once()


def test_has_treatment_cohort_membership_calls_api_delivery_and_logs(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")

    client = create_default_client()

    cm = CohortMembership("testing", CohortArm.TREATMENT)

    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(request=req, only_log=False, experiment=cm)

    api_patch.return_value = Response(insertion=req.insertion)

    resp = client.deliver(dreq)
    assert resp is not None
    assert req.client_request_id
    assert len(resp.response.insertion) == 10
    assert resp.execution_server == ExecutionServer.API

    # Cohort membership and server side delivery -> follow-up logging.
    sdk_patch.assert_not_called()
    metrics_patch.assert_called_once()
    api_patch.assert_called_once()

    # No need to send a delivery log since delivery happened server-side.
    log_request: LogRequest = metrics_patch.call_args[0][0]
    assert len(log_request.delivery_log) == 0


def test_has_control_cohort_membership_calls_sdk_delivery_and_logs(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")

    client = create_default_client()

    cm = CohortMembership("testing", CohortArm.CONTROL)

    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(request=req, only_log=False, experiment=cm)

    sdk_patch.return_value = Response(insertion=req.insertion)

    resp = client.deliver(dreq)
    assert resp is not None
    assert req.client_request_id
    assert len(resp.response.insertion) == 10
    assert resp.execution_server == ExecutionServer.SDK

    sdk_patch.assert_called_once()
    metrics_patch.assert_called_once()
    api_patch.assert_not_called()

    assert_sdk_log_request(req, resp.response, metrics_patch.call_args[0][0])


def test_api_delivery_error_falls_back_to_sdk_delivery(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")

    client = create_default_client()

    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(request=req, only_log=False)

    sdk_patch.return_value = Response(insertion=req.insertion)
    api_patch.side_effect = Exception("oops")

    resp = client.deliver(dreq)
    assert resp is not None
    assert req.client_request_id
    assert len(resp.response.insertion) == 10
    assert resp.execution_server == ExecutionServer.SDK

    sdk_patch.assert_called_once()
    metrics_patch.assert_called_once()
    api_patch.assert_called_once()

    assert_sdk_log_request(req, resp.response, metrics_patch.call_args[0][0])


def assert_sdk_log_request(req: Request, resp: Response, log_request: LogRequest):
    assert len(log_request.delivery_log) == 1
    assert log_request.delivery_log[0].request == req
    assert log_request.delivery_log[0].response == resp
    assert log_request.delivery_log[0].execution.execution_server == ExecutionServer.SDK


def create_default_client() -> PromotedDeliveryClient:
    client = PromotedDeliveryClient("", "", "", "")
    client.executor = DummyExecutor()  # type: ignore
    return client
