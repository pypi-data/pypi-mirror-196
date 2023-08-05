from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from typing import Any, Optional
from vesselapi import utils


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class EventAttendeeAssociations:
    association_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('associationId') }})
    event_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('eventId') }})
    

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class EventAttendee:
    r"""EventAttendee
    Event Attendees hold information about someone who attendeed or was invited to an event. Attendees are always associated with some Event and another person object such as a Contact, Lead, or Other.
    """
    
    associated_object_type: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('associatedObjectType') }})
    associations: EventAttendeeAssociations = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('associations') }})
    created_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('createdTime') }})
    id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('id') }})
    modified_time: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('modifiedTime') }})
    native_id: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('nativeId') }})
    additional: Optional[dict[str, Any]] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('additional'), 'exclude': lambda f: f is None }})
    email: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('email'), 'exclude': lambda f: f is None }})
    status: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('status'), 'exclude': lambda f: f is None }})
    