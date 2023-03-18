import pytest
from promoted_python_delivery_client.model.insertion import Insertion
from promoted_python_delivery_client.model.properties import Properties
from promoted_python_delivery_client.model.request import Request
from promoted_python_delivery_client.model.user_info import UserInfo
from promoted_python_delivery_client.client.serde import delivery_request_to_json, delivery_request_to_json_2, delivery_request_to_json_3, delivery_reponse_from_json_2


def test_delivery_request_to_json():
    req = _build_request()
    for _ in range(10):
        payload = delivery_request_to_json(req)
        print(payload)


def test_delivery_request_to_json_2():
    req = _build_request()
    for _ in range(10):
        payload = delivery_request_to_json_2(req)
        print(payload)


def test_delivery_request_to_json_3():
    req = _build_request()
    for _ in range(10):
        payload = delivery_request_to_json_3(req)
        print(payload)


def test_delivery_request_to_json_3_allows_null_properties():
    req = Request(insertion=[Insertion(content_id="a", properties=Properties({"xyz": None, "abc": "zzz"}))])
    payload = delivery_request_to_json_3(req)
    assert "abc" in payload
    assert "zzz" in payload
    assert "xyz" in payload


def test_delivery_request_to_json_has_no_nulls():
    req = _build_request()
    payload = delivery_request_to_json_3(req)
    assert "null" not in payload

    payload = delivery_request_to_json_2(req)
    assert "null" not in payload

    payload = delivery_request_to_json(req)
    assert "null" not in payload


def _build_request() -> Request:
    insertion = [
        Insertion(content_id="28835", properties=Properties(struct={"price": 1.23})),
        Insertion(content_id="57076", properties=Properties(struct={"price": "4.56"})),
        Insertion(content_id="37796", properties=Properties(struct={"price": 0})),
        Insertion(content_id="49815"),
      ]
    # Pad it out to 100 total insertions
    for num in range(96):
        insertion.append(Insertion(content_id=str(num).rjust(5, '0')))
    return Request(insertion=insertion, user_info=UserInfo(log_user_id="abc"))


def test_delivery_request_with_insertion_matrix_to_json():
    req = Request(insertion_matrix_headers=["abc", "d.e.f"], insertion_matrix=[["12", 34],
                                                                               ["56", 78]])
    payload = delivery_request_to_json_3(req)

    assert "abc" in payload
    assert "d.e.f" in payload
    assert "12" in payload
    assert "34" in payload
    assert "56" in payload
    assert "78" in payload

    assert "null" not in payload

def test_delivery_request_with_insertion_matrix_to_json_keeps_empty():
    req = Request(insertion_matrix_headers=["a"], insertion_matrix=[[None]])
    payload = delivery_request_to_json_3(req)

    assert "[[null]]" in payload


def test_delivery_reponse_from_json_2():
    response = delivery_reponse_from_json_2(
        '{"requestId":"reqid", "insertion": []}'.encode('utf-8'))
    assert response.request_id == 'reqid'
    assert len(response.insertion) == 0


def test_delivery_reponse_from_json_2_empty():
    with pytest.raises(KeyError) as ex:
        response = delivery_reponse_from_json_2('{}'.encode('utf-8'))
    assert "request_id" in str(ex)


def test_delivery_reponse_from_json_2_no_insertions():
    response = delivery_reponse_from_json_2('{"requestId":"reqid"}'.encode('utf-8'))
    assert response.request_id == 'reqid'
    assert len(response.insertion) == 0