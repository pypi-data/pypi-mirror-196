from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from typing import Any, Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class EventUpdate:
    additional: Optional[dict[str, Any]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('additional'), 'exclude': lambda f: f is None }})
    description: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('description'), 'exclude': lambda f: f is None }})
    end_date_time: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('endDateTime'), 'exclude': lambda f: f is None }})
    is_all_day_event: Optional[bool] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('isAllDayEvent'), 'exclude': lambda f: f is None }})
    location: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('location'), 'exclude': lambda f: f is None }})
    owner_user_id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('ownerUserId'), 'exclude': lambda f: f is None }})
    start_date_time: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('startDateTime'), 'exclude': lambda f: f is None }})
    subject: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('subject'), 'exclude': lambda f: f is None }})
    type: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('type'), 'exclude': lambda f: f is None }})
    