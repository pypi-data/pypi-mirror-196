from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Optional
from writer import utils

class TermMistakePosEnum(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADVERB = "adverb"
    ADJECTIVE = "adjective"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class TermMistake:
    case_sensitive: bool = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('caseSensitive') }})
    mistake: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('mistake') }})
    term_bank_id: int = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('termBankId') }})
    term_id: int = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('termId') }})
    id: Optional[int] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id'), 'exclude': lambda f: f is None }})
    pos: Optional[TermMistakePosEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('pos'), 'exclude': lambda f: f is None }})
    