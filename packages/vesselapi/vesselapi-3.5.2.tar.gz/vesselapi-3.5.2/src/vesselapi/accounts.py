import requests as requests_http
from . import utils
from typing import Optional
from vesselapi.models import operations

class Accounts:
    _client: requests_http.Session
    _security_client: requests_http.Session
    _server_url: str
    _language: str
    _sdk_version: str
    _gen_version: str

    def __init__(self, client: requests_http.Session, security_client: requests_http.Session, server_url: str, language: str, sdk_version: str, gen_version: str) -> None:
        self._client = client
        self._security_client = security_client
        self._server_url = server_url
        self._language = language
        self._sdk_version = sdk_version
        self._gen_version = gen_version
        
    def batch(self, request: operations.GetBatchCrmAccountRequest) -> operations.GetBatchCrmAccountResponse:
        r"""Get Batch Accounts
        Retrieve Accounts by a set of Id's
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/account/batch'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetBatchCrmAccountResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetBatchCrmAccountResponseBody])
                res.response_body = out

        return res

    def create(self, request: operations.PostCrmAccountRequest) -> operations.PostCrmAccountResponse:
        r"""Create Account
        Create a new Account
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/account'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        
        client = self._security_client
        
        http_res = client.request('POST', url, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.PostCrmAccountResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.PostCrmAccountResponseBody])
                res.response_body = out

        return res

    def details(self, request: operations.GetDetailsCrmAccountRequest) -> operations.GetDetailsCrmAccountResponse:
        r"""Get Account Details
        Get details about all accounts. 
        Details include the type, possible values, and other meta data about the fields.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/account/details'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetDetailsCrmAccountResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetDetailsCrmAccountResponseBody])
                res.response_body = out

        return res

    def find(self, request: operations.GetOneCrmAccountRequest) -> operations.GetOneCrmAccountResponse:
        r"""Get Account
        Retrieve a single Account by Id
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/account'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetOneCrmAccountResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetOneCrmAccountResponseBody])
                res.response_body = out

        return res

    def list(self, request: operations.GetAllCrmAccountsRequest) -> operations.GetAllCrmAccountsResponse:
        r"""Get All Accounts
        Retrieve all Accounts
        *CRM Caveats*:
        - Pipedrive: dealIds + contactIds not supported when querying for all accounts
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/accounts'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetAllCrmAccountsResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetAllCrmAccountsResponseBody])
                res.response_body = out

        return res

    def search(self, request: operations.SearchCrmAccountsRequest) -> operations.SearchCrmAccountsResponse:
        r"""Search Accounts
        Search all Accounts using filters
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/accounts/search'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('POST', url, params=query_params, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.SearchCrmAccountsResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.SearchCrmAccountsResponseBody])
                res.response_body = out

        return res

    def update(self, request: operations.PutCrmAccountRequest) -> operations.PutCrmAccountResponse:
        r"""Update Account
        Update an existing Account
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/account'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        
        client = self._security_client
        
        http_res = client.request('PATCH', url, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.PutCrmAccountResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.PutCrmAccountResponseBody])
                res.response_body = out

        return res

    