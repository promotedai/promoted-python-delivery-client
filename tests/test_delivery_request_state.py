from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.client.delivery_request_state import DeliveryRequestState
from promoted_python_delivery_client.model.request import Request
from tests.utils_testing import create_test_request_insertions


def test_exactly_max_request_insertions():
    insertion = create_test_request_insertions(10)
    req = Request(insertion=insertion)

    state = DeliveryRequestState(DeliveryRequest(req))
    to_send = state.get_request_to_send(10)
    assert len(to_send.insertion) == 10


def test_more_than_max_request_insertions():
    insertion = create_test_request_insertions(10)
    req = Request(insertion=insertion)

    state = DeliveryRequestState(DeliveryRequest(req))
    to_send = state.get_request_to_send(5)
    assert len(to_send.insertion) == 5


def test_exactly_max_request_insertions_with_matrix():
    req = Request(insertion_matrix_headers=["contentId"],
                  insertion_matrix=[["0"], ["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"], ["8"], ["9"]])

    state = DeliveryRequestState(DeliveryRequest(req))
    to_send = state.get_request_to_send(10)
    assert len(to_send.insertion_matrix) == 10


def test_more_than_max_request_insertions_with_matrix():
    req = Request(insertion_matrix_headers=["contentId"],
                  insertion_matrix=[["0"], ["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"], ["8"], ["9"]])

    state = DeliveryRequestState(DeliveryRequest(req))
    to_send = state.get_request_to_send(5)
    assert len(to_send.insertion_matrix) == 5
