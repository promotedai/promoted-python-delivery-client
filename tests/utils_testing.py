
from typing import List

from promoted_python_delivery_client.model.insertion import Insertion


def create_test_request_insertions(num: int) -> List[Insertion]:
    ins: List[Insertion] = []
    for i in range(0, num):
        ins.append(Insertion(content_id=str(i)))
    return ins
