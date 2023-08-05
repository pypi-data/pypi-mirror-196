from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Optional
from writer import utils

class TermMistakeCreatePosEnum(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADVERB = "adverb"
    ADJECTIVE = "adjective"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class TermMistakeCreate:
    case_sensitive: bool = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('caseSensitive') }})
    mistake: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('mistake') }})
    pos: Optional[TermMistakeCreatePosEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('pos'), 'exclude': lambda f: f is None }})
    reference: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('reference'), 'exclude': lambda f: f is None }})
    