from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from writer import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class TermTagResponse:
    id: int = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    parent_tag_id: int = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('parentTagId') }})
    tag: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('tag') }})
    term_id: int = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('termId') }})
    