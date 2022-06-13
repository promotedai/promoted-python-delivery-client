import pytest
from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.client.insertion_page_type import InsertionPageType
from promoted_python_delivery_client.client.sdk_delivery import SDKDelivery
from promoted_python_delivery_client.model.paging import Paging
from promoted_python_delivery_client.model.request import Request
from tests.utils_testing import create_test_request_insertions


def test_invalid_paging_offset():
    req = Request(insertion=create_test_request_insertions(10),
                  paging=Paging(size=10, offset=10))
    dreq = DeliveryRequest(req)
    with pytest.raises(ValueError) as ex:
        SDKDelivery().run_delivery(dreq)
        assert str(ex) == "Invalid paging"


def test_no_paging_returns_all():
    req = Request(insertion=create_test_request_insertions(10))
    dreq = DeliveryRequest(req)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 10


def test_paging_zero_size_returns_all():
    req = Request(insertion=create_test_request_insertions(10),
                  paging=Paging(size=0))
    dreq = DeliveryRequest(req)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 10


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


def test_pre_paged():
    req = Request(insertion=create_test_request_insertions(10),
                  paging=Paging(size=0, offset=5))
    dreq = DeliveryRequest(req, insertion_page_type=InsertionPageType.PREPAGED)
    resp = SDKDelivery().run_delivery(dreq)
    assert req.request_id is not None
    assert len(req.request_id) > 0
    assert len(resp.insertion) == 10
    for i in range(0, 10):
        assert resp.insertion[i].position == i+5
