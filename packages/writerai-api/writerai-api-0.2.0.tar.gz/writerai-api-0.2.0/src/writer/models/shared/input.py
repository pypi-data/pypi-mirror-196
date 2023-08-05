from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Optional
from writer import utils

class InputTypeEnum(str, Enum):
    TEXTBOX = "textbox"
    TEXTAREA = "textarea"
    DROPDOWN = "dropdown"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class Input:
    dynamic: bool = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('dynamic') }})
    name: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('name') }})
    required: bool = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('required') }})
    type: InputTypeEnum = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('type') }})
    help: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('help'), 'exclude': lambda f: f is None }})
    max_fields: Optional[int] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('maxFields'), 'exclude': lambda f: f is None }})
    min_fields: Optional[int] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('minFields'), 'exclude': lambda f: f is None }})
    options: Optional[list[str]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('options'), 'exclude': lambda f: f is None }})
    subtitle: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('subtitle'), 'exclude': lambda f: f is None }})
    unit_copy: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('unitCopy'), 'exclude': lambda f: f is None }})
    