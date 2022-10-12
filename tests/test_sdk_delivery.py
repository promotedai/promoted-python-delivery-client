import pytest
from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.client.sdk_delivery import SDKDelivery
from promoted_python_delivery_client.model.insertion import Insertion
from promoted_python_delivery_client.model.paging import Paging
from promoted_python_delivery_client.model.properties import Properties
from promoted_python_delivery_client.model.request import Request
from tests.utils_testing import create_test_request_insertions


def test_invalid_paging_offset_and_insertion_start():
    req = Request(insertion=create_test_request_insertions(10),
                  paging=Paging(size=10, offset=5))
    dreq = DeliveryRequest(req, insertion_start=100)
    with pytest.raises(ValueError) as ex:
        SDKDelivery().run_delivery(dreq)
    assert "offset should be >= insertion start" in str(ex)


def test_valid_paging_offset_and_insertion_start():
    req = Request(insertion=create_test_request_insertions(10),
                  paging=Paging(size=10, offset=5))
    dreq = DeliveryRequest(req, insertion_start=5)
    SDKDelivery().run_delivery(dreq)


def test_response_insertions_only_have_key_fields():
    insertions = create_test_request_insertions(1)
    req_ins = insertions[0]
    req_ins.properties = Properties({"a": True})
    req_ins.retrieval_rank = 3
    req_ins.retrieval_score = 2.2

    req = Request(insertion=insertions)
    dreq = DeliveryRequest(req)
    resp = SDKDelivery().run_delivery(dreq)

    resp_ins = resp.insertion[0]
    assert resp_ins.content_id == req_ins.content_id
    assert resp_ins.properties is None
    assert resp_ins.retrieval_rank is None
    assert resp_ins.retrieval_score is None

    assert req_ins.properties is not None
    assert req_ins.retrieval_rank is not None
    assert req_ins.retrieval_score is not None


def test_no_paging_returns_all():
    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(req)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 10
    for i in range(0, 10):
        assert resp.insertion[i].position == i
        assert resp.insertion[i].insertion_id


def test_paging_zero_size_returns_all():
    req = Request(insertion=create_test_request_insertions(10),
                  paging=Paging(size=0))
    dreq = DeliveryRequest(req)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 10
    for i in range(0, 10):
        assert resp.insertion[i].position == i
        assert resp.insertion[i].insertion_id


def test_paging_zero_offset():
    req = Request(insertion=create_test_request_insertions(10),
                  paging=Paging(size=5, offset=0))
    dreq = DeliveryRequest(req)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 5
    for i in range(0, 5):
        assert resp.insertion[i].position == i
        assert resp.insertion[i].insertion_id


def test_paging_non_zero_offset():
    req = Request(insertion=create_test_request_insertions(10),
                  paging=Paging(size=5, offset=5))
    dreq = DeliveryRequest(req)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 5
    for i in range(5, 10):
        assert resp.insertion[i-5].position == i
        assert resp.insertion[i-5].insertion_id


def test_paging_size_more_than_insertions():
    req = Request(insertion=create_test_request_insertions(10),
                  paging=Paging(size=11, offset=0))
    dreq = DeliveryRequest(req)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 10
    for i in range(0, 10):
        assert resp.insertion[i].position == i
        assert resp.insertion[i].insertion_id


def test_insertion_start_set_to_offset():
    insertion_start = 5
    req = Request(insertion=create_test_request_insertions(3),
                  paging=Paging(size=2, offset=5))
    dreq = DeliveryRequest(req, insertion_start=insertion_start)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 2

    # Returns positions 0 and 1 since we want an offset identical to the request insertion start.
    for idx, ins in enumerate(resp.insertion):
        assert ins.position == insertion_start + idx
        assert ins.content_id == str(idx)


def test_insertion_start_less_than_offset():
    insertion_start = 5
    offset_diff = 1
    req = Request(insertion=create_test_request_insertions(3),
                  paging=Paging(size=2, offset=6))
    dreq = DeliveryRequest(req, insertion_start=insertion_start)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 2

    # Returns positions 1 and 2 since we want an offset one past the request insertion start.
    for idx, ins in enumerate(resp.insertion):
        assert ins.position == insertion_start + offset_diff + idx
        assert ins.content_id == str(idx+offset_diff)


def test_insertion_start_with_offset_outside_size():
    insertion_start = 5
    req = Request(insertion=create_test_request_insertions(3),
                  paging=Paging(size=2, offset=8))
    dreq = DeliveryRequest(req, insertion_start=insertion_start)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    # Returns empty
    assert len(resp.insertion) == 0


def test_response_insertions_only_have_key_fields2():
    req = Request(insertion_matrix_headers=["somethingElse", "contentId"], insertion_matrix=[["a", "b"], ["c", "d"]])
    dreq = DeliveryRequest(req)
    resp = SDKDelivery().run_delivery(dreq)

    assert resp.insertion[0].content_id == "b"
    assert resp.insertion[1].content_id == "d"
