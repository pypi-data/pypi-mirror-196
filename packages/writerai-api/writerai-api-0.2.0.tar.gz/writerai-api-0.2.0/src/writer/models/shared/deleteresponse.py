from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from writer import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class DeleteResponse:
    deleted: int = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('deleted') }})
    