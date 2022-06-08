from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import List, Optional
from promoted_python_delivery_client.model.client_info import ClientInfo
from promoted_python_delivery_client.model.delivery_log import DeliveryLog
from promoted_python_delivery_client.model.cohort_membership import CohortMembership
from promoted_python_delivery_client.model.timing import Timing
from promoted_python_delivery_client.model.user_info import UserInfo


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LogRequest:
    delivery_log: List[DeliveryLog]
    cohort_membership: Optional[List[CohortMembership]]
    user_info: Optional[UserInfo]
    client_info: Optional[ClientInfo]
    platform_id: Optional[int]
    timing: Optional[Timing]
