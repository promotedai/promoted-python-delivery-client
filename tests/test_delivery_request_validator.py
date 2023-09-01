from promoted_python_delivery_client.client.delivery_request import DeliveryRequest
from promoted_python_delivery_client.client.delivery_request_validator import DeliveryRequestValidator
from promoted_python_delivery_client.model.cohort_arm import CohortArm
from promoted_python_delivery_client.model.cohort_membership import CohortMembership
from promoted_python_delivery_client.model.insertion import Insertion
from promoted_python_delivery_client.model.paging import Paging
from promoted_python_delivery_client.model.request import Request
from promoted_python_delivery_client.model.user_info import UserInfo


def test_request_must_be_set():
    req = DeliveryRequest(request=None)  # type: ignore
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Request must be set"


def test_validate_request_id_must_be_unset_on_request():
    req = DeliveryRequest(
        Request(insertion=[], user_info=UserInfo(anon_user_id="a"), request_id="zzz"),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Request.requestId should not be set"


def test_validate_insertion_id_must_be_unset():
    req = DeliveryRequest(
        Request(insertion=[Insertion(content_id="a", insertion_id="b")], user_info=UserInfo(anon_user_id="a")),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Insertion.insertionId should not be set"


def test_validate_insertion_start_must_be_non_neg():
    req = DeliveryRequest(
        Request(insertion=[Insertion(content_id="a")], user_info=UserInfo(anon_user_id="a")),
        only_log=False,
        insertion_start=-1)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Insertion start must be greater or equal to 0"


def test_validate_content_id_must_be_set():
    req = DeliveryRequest(
        Request(insertion=[Insertion(content_id="")], user_info=UserInfo(anon_user_id="a")),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Insertion.contentId should be set"


def test_validate_with_valid_insertion():
    req = DeliveryRequest(
        Request(insertion=[Insertion(content_id="a")], user_info=UserInfo(anon_user_id="a")),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 0


def test_validate_experiment_valid():
    req = DeliveryRequest(
        Request(insertion=[Insertion(content_id="a")], user_info=UserInfo(anon_user_id="a")),
        only_log=False,
        experiment=CohortMembership("my cohort", CohortArm.TREATMENT))
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 0


def test_validate_user_info_on_request():
    req = DeliveryRequest(
        Request(insertion=[Insertion(content_id="a")]),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Request.userInfo should be set"


def test_validate_anon_user_id_on_request():
    req = DeliveryRequest(
        Request(insertion=[Insertion(content_id="a")], user_info=UserInfo(anon_user_id="")),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Request.userInfo.anonUserId should be set"


def test_validate_captures_multiple_errors():
    req = DeliveryRequest(
        Request(insertion=[Insertion(content_id="a")], user_info=UserInfo(anon_user_id=""), request_id="z"),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 2
    assert errors[0] == "Request.requestId should not be set"
    assert errors[1] == "Request.userInfo.anonUserId should be set"


def test_validate_with_only_matrix_headers():
    req = DeliveryRequest(
        Request(insertion_matrix_headers=["contentId"], user_info=UserInfo(anon_user_id="a")),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Request.insertionMatrixHeaders and Request.insertionMatrix should be used together"


def test_validate_with_plain_and_matrix_insertions():
    req = DeliveryRequest(
        Request(insertion_matrix_headers=["contentId"], insertion_matrix=[["b"]],
                insertion=[Insertion(content_id="a")], user_info=UserInfo(anon_user_id="a")),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Request.insertion will be ignored because Request.insertionMatrix is present"


def test_validate_with_invalid_matrix_header():
    req = DeliveryRequest(
        Request(insertion_matrix_headers=["insertionId", "contentId"], insertion_matrix=[["b", "c"]], user_info=UserInfo(anon_user_id="a")),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Request.insertionMatrixHeaders should not specify insertionId"


def test_validate_with_invalid_matrix_header():
    req = DeliveryRequest(
        Request(insertion_matrix_headers=["d"], insertion_matrix=[["b"]], user_info=UserInfo(anon_user_id="a")),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 1
    assert errors[0] == "Request.insertionMatrixHeaders should specify contentId"


def test_validate_with_valid_matrix():
    req = DeliveryRequest(
        Request(insertion_matrix_headers=["contentId"], insertion_matrix=[["b"]], user_info=UserInfo(anon_user_id="a")),
        only_log=False)
    errors = DeliveryRequestValidator().validate(req, False)
    assert len(errors) == 0
