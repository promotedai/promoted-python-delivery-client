from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import Optional
from promoted_python_delivery_client.model.client_info import ClientInfo
from promoted_python_delivery_client.model.properties import Properties
from promoted_python_delivery_client.model.timing import Timing
from promoted_python_delivery_client.model.user_info import UserInfo


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Insertion:
    content_id: str
    position: Optional[int] = None
    insertion_id: Optional[str] = None
    retrieval_rank: Optional[int] = None
    retrieval_score: Optional[float] = None
    view_id: Optional[str] = None
    user_info: Optional[UserInfo] = None
    client_info: Optional[ClientInfo] = None
    auto_view_id: Optional[str] = None
    platform_id: Optional[str] = None
    properties: Optional[Properties] = None
    session_id: Optional[str] = None
    timing: Optional[Timing] = None
