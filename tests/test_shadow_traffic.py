from pytest_mock.plugin import MockerFixture
from promoted_python_delivery_client.client.client import PromotedDeliveryClient
from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.model.client_info import ClientInfo
from promoted_python_delivery_client.model.cohort_arm import CohortArm
from promoted_python_delivery_client.model.cohort_membership import CohortMembership
from promoted_python_delivery_client.model.request import Request
from promoted_python_delivery_client.model.traffic_type import TrafficType
from tests.dummy_executor import DummyExecutor
from tests.utils_testing import create_test_request_insertions


def test_send_shadow_traffic_for_only_log_sampled_in(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")
    uniform_patch = mocker.patch("random.uniform")

    client = create_default_client(0.5)

    req = Request(insertion=create_test_request_insertions(10), client_info=ClientInfo(traffic_type=TrafficType.PRODUCTION))
    dreq = DeliveryRequest(request=req, only_log=True)

    uniform_patch.return_value = 0.3  # sampled in

    client.deliver(dreq)

    sdk_patch.assert_called_once()
    metrics_patch.assert_called_once()
    api_patch.assert_called_once()

    # There should be two executor calls, one from metrics and one from shadow traffic.
    assert client.executor.calls == 2  # type: ignore

    dreq: DeliveryRequest = api_patch.call_args[0][0]
    assert dreq.request.client_info is not None
    assert dreq.request.client_info.traffic_type == TrafficType.SHADOW


def test_send_shadow_traffic_for_user_in_control(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")
    uniform_patch = mocker.patch("random.uniform")

    client = create_default_client(0.5)
    cm = CohortMembership("testing", CohortArm.CONTROL)

    req = Request(insertion=create_test_request_insertions(10), client_info=ClientInfo(traffic_type=TrafficType.PRODUCTION))
    dreq = DeliveryRequest(request=req, only_log=False, experiment=cm)

    uniform_patch.return_value = 0.3  # sampled in

    client.deliver(dreq)

    sdk_patch.assert_called_once()
    metrics_patch.assert_called_once()
    api_patch.assert_called_once()

    dreq: DeliveryRequest = api_patch.call_args[0][0]
    assert dreq.request.client_info is not None
    assert dreq.request.client_info.traffic_type == TrafficType.SHADOW


def test_dont_send_shadow_traffic_sampled_out(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")
    uniform_patch = mocker.patch("random.uniform")

    client = create_default_client(0.5)

    req = Request(insertion=create_test_request_insertions(10), client_info=ClientInfo(traffic_type=TrafficType.PRODUCTION))
    dreq = DeliveryRequest(request=req, only_log=True)

    uniform_patch.return_value = 0.7  # sampled out

    client.deliver(dreq)

    sdk_patch.assert_called_once()
    metrics_patch.assert_called_once()
    api_patch.assert_not_called()


def test_dont_send_shadow_traffic_for_user_in_treatment(mocker: MockerFixture):
    # This case calls normal delivery successfully
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")
    uniform_patch = mocker.patch("random.uniform")

    client = create_default_client(0.5)

    req = Request(insertion=create_test_request_insertions(10), client_info=ClientInfo(traffic_type=TrafficType.PRODUCTION))
    dreq = DeliveryRequest(request=req, only_log=False)

    uniform_patch.return_value = 0.7  # sampled out

    client.deliver(dreq)

    sdk_patch.assert_not_called()
    metrics_patch.assert_not_called()
    api_patch.assert_called_once()


def test_dont_send_shadow_traffic_for_only_log_when_turned_off(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")
    uniform_patch = mocker.patch("random.uniform")

    client = create_default_client(0)

    req = Request(insertion=create_test_request_insertions(10), client_info=ClientInfo(traffic_type=TrafficType.PRODUCTION))
    dreq = DeliveryRequest(request=req, only_log=True)

    uniform_patch.return_value = 0.3  # sampled in

    client.deliver(dreq)

    sdk_patch.assert_called_once()
    metrics_patch.assert_called_once()
    api_patch.assert_not_called()


def test_blocking_shadow_traffic(mocker: MockerFixture):
    api_patch = mocker.patch("promoted_python_delivery_client.client.api_delivery.APIDelivery.run_delivery")
    sdk_patch = mocker.patch("promoted_python_delivery_client.client.sdk_delivery.SDKDelivery.run_delivery")
    metrics_patch = mocker.patch("promoted_python_delivery_client.client.api_metrics.APIMetrics.run_metrics_logging")
    uniform_patch = mocker.patch("random.uniform")

    client = create_default_client(0.5)
    client.blocking_shadow_traffic = True

    req = Request(insertion=create_test_request_insertions(10), client_info=ClientInfo(traffic_type=TrafficType.PRODUCTION))
    dreq = DeliveryRequest(request=req, only_log=True)

    uniform_patch.return_value = 0.3  # sampled in

    client.deliver(dreq)

    sdk_patch.assert_called_once()
    metrics_patch.assert_called_once()
    api_patch.assert_called_once()

    # There should be one executor call from metrics, none from shadow traffic.
    assert client.executor.calls == 1  # type: ignore

    dreq: DeliveryRequest = api_patch.call_args[0][0]
    assert dreq.request.client_info is not None
    assert dreq.request.client_info.traffic_type == TrafficType.SHADOW


def create_default_client(shadow_traffic_rate: float) -> PromotedDeliveryClient:
    client = PromotedDeliveryClient("", "", "", "", shadow_traffic_delivery_rate=shadow_traffic_rate)
    client.executor = DummyExecutor()  # type: ignore
    return client
