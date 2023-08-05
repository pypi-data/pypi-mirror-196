from __future__ import annotations
import dataclasses
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Optional
from vesselapi import utils

class ConnectionIntegrationIDEnum(str, Enum):
    SALESFORCE = "salesforce"
    HUBSPOT = "hubspot"
    PIPEDRIVE = "pipedrive"

class ConnectionStatusEnum(str, Enum):
    NEW_CONNECTION = "NEW_CONNECTION"
    INITIAL_SYNC = "INITIAL_SYNC"
    READY = "READY"


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class Connection:
    connection_id: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('connectionId'), 'exclude': lambda f: f is None }})
    created_time: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('createdTime'), 'exclude': lambda f: f is None }})
    integration_id: Optional[ConnectionIntegrationIDEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('integrationId'), 'exclude': lambda f: f is None }})
    last_activity_date: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('lastActivityDate'), 'exclude': lambda f: f is None }})
    native_org_url: Optional[str] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('nativeOrgURL'), 'exclude': lambda f: f is None }})
    status: Optional[ConnectionStatusEnum] = dataclasses.field(default=None, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('status'), 'exclude': lambda f: f is None }})
    