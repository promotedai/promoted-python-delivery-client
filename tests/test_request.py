from promoted_python_delivery_client.model.insertion import Insertion
from promoted_python_delivery_client.model.request import Request
from promoted_python_delivery_client.model.user_info import UserInfo


def test_to_json_has_no_nones():
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

    data = req.to_json()  # type: ignore this is from dataclass_json
    assert "None" not in data
