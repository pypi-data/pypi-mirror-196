from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Optional
from writer import utils

class TermExampleTypeEnum(str, Enum):
    GOOD = "good"
    BAD = "bad"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class TermExample:
    example: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('example') }})
    term_bank_id: int = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('termBankId') }})
    term_id: int = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('termId') }})
    type: TermExampleTypeEnum = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('type') }})
    id: Optional[int] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id'), 'exclude': lambda f: f is None }})
    