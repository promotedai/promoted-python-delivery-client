from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import Optional


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UserInfo:
    user_id: Optional[str] = None
    log_user_id: Optional[str] = None
    is_internal_user: Optional[bool] = None
