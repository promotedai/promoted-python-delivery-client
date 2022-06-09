from promoted_python_delivery_client.model.request import Request
from promoted_python_delivery_client.model.user_info import UserInfo
from tests.utils_testing import create_test_request_insertions


def test_to_json_has_no_nones():
    insertion = create_test_request_insertions(10)
    req = Request(insertion=insertion, user_info=UserInfo(log_user_id="abc"))

    data = req.to_json()  # type: ignore this is from dataclass_json
    assert "None" not in data
