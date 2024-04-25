from promoted_python_delivery_client.client.api_metrics import is_success_status_code


def test_max_threshold():
    assert is_success_status_code(100) is False
    assert is_success_status_code(200) is True
    assert is_success_status_code(202) is True
    assert is_success_status_code(299) is True
    assert is_success_status_code(300) is False
    assert is_success_status_code(404) is False
    assert is_success_status_code(502) is False
