__doc__ = """ SDK Documentation: Vessel's APIs requires an access token to be used together with your Vessel API token. Ensure the following headers are provided when making API calls:

Key | Value | Description
---------|----------|----------
 vessel-api-token | `<VESSEL_API_TOKEN>` | The API token provided by us
 
Additionally, in the query or body parameters of each request depending on whether it is a GET or POST, make sure to include the `accessToken` for the connection you want to access."""
import requests as requests_http
from . import utils
from .accounts import Accounts
from .attendees import Attendees
from .connections import Connections
from .contacts import Contacts
from .deals import Deals
from .emails import Emails
from .events import Events
from .integrations import Integrations
from .leads import Leads
from .links import Links
from .notes import Notes
from .passthrough import Passthrough
from .tasks import Tasks
from .tokens import Tokens
from .users import Users
from .webhooks import Webhooks
from vesselapi.models import shared

SERVERS = [
	"https://api.vessel.land",
]

class VesselAPI:
    r"""SDK Documentation: Vessel's APIs requires an access token to be used together with your Vessel API token. Ensure the following headers are provided when making API calls:
    
    Key | Value | Description
    ---------|----------|----------
     vessel-api-token | `<VESSEL_API_TOKEN>` | The API token provided by us
     
    Additionally, in the query or body parameters of each request depending on whether it is a GET or POST, make sure to include the `accessToken` for the connection you want to access."""
    accounts: Accounts
    attendees: Attendees
    connections: Connections
    contacts: Contacts
    deals: Deals
    emails: Emails
    events: Events
    integrations: Integrations
    leads: Leads
    links: Links
    notes: Notes
    passthrough: Passthrough
    tasks: Tasks
    tokens: Tokens
    users: Users
    webhooks: Webhooks
    
    _client: requests_http.Session
    _security_client: requests_http.Session
    _security: shared.Security
    _server_url: str = SERVERS[0]
    _language: str = "python"
    _sdk_version: str = "3.5.2"
    _gen_version: str = "1.8.5"

    def __init__(self) -> None:
        self._client = requests_http.Session()
        self._security_client = requests_http.Session()
        self._init_sdks()

    def config_server_url(self, server_url: str, params: dict[str, str] = None):
        if params is not None:
            self._server_url = utils.template_url(server_url, params)
        else:
            self._server_url = server_url

        self._init_sdks()
    
    

    def config_client(self, client: requests_http.Session):
        self._client = client
        
        if self._security is not None:
            self._security_client = utils.configure_security_client(self._client, self._security)
        self._init_sdks()
    
    def config_security(self, security: shared.Security):
        self._security = security
        self._security_client = utils.configure_security_client(self._client, security)
        self._init_sdks()
    
    def _init_sdks(self):
        self.accounts = Accounts(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.attendees = Attendees(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.connections = Connections(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.contacts = Contacts(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.deals = Deals(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.emails = Emails(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.events = Events(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.integrations = Integrations(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.leads = Leads(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.links = Links(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.notes = Notes(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.passthrough = Passthrough(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.tasks = Tasks(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.tokens = Tokens(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.users = Users(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
        self.webhooks = Webhooks(
            self._client,
            self._security_client,
            self._server_url,
            self._language,
            self._sdk_version,
            self._gen_version
        )
        
    