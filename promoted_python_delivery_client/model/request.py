from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import List, Optional
from promoted_python_delivery_client.model.blender_config import BlenderConfig
from promoted_python_delivery_client.model.client_info import ClientInfo
from promoted_python_delivery_client.model.insertion import Insertion
from promoted_python_delivery_client.model.paging import Paging
from promoted_python_delivery_client.model.properties import Properties
from promoted_python_delivery_client.model.timing import Timing
from promoted_python_delivery_client.model.use_case import UseCase
from promoted_python_delivery_client.model.user_info import UserInfo


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Request:
    insertion: List[Insertion]
    user_info: Optional[UserInfo] = None
    client_request_id: Optional[str] = None
    request_id: Optional[str] = None
    client_info: Optional[ClientInfo] = None
    search_query: Optional[str] = None
    use_case: Optional[UseCase] = None
    auto_view_id: Optional[str] = None
    blender_config: Optional[BlenderConfig] = None
    debug: Optional[bool] = None
    paging: Optional[Paging] = None
    platform_id: Optional[int] = None
    properties: Optional[Properties] = None
    session_id: Optional[str] = None
    timing: Optional[Timing] = None
    view_id: Optional[str] = None
