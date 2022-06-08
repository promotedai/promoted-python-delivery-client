from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import Optional
from promoted_python_delivery_client.model.cohort_arm import CohortArm
from promoted_python_delivery_client.model.timing import Timing
from promoted_python_delivery_client.model.user_info import UserInfo


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CohortMembership:
    cohort_id: str
    arm: CohortArm
    platform_id: Optional[int] = None
    user_info: Optional[UserInfo] = None
    timing: Optional[Timing] = None
