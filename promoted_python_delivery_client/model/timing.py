from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import Optional


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Timing:
    client_log_timestamp: Optional[int] = None
    event_api_timestamp: Optional[int] = None
    log_timestamp: Optional[int] = None
