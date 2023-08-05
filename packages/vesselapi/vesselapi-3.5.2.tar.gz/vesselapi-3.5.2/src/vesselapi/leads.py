import requests as requests_http
from . import utils
from typing import Optional
from vesselapi.models import operations

class Leads:
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
        
    def batch(self, request: operations.GetBatchCrmLeadRequest) -> operations.GetBatchCrmLeadResponse:
        r"""Get Batch Leads
        Retrieve Leads by a set of Id's
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/lead/batch'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetBatchCrmLeadResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetBatchCrmLeadResponseBody])
                res.response_body = out

        return res

    def create(self, request: operations.PostCrmLeadRequest) -> operations.PostCrmLeadResponse:
        r"""Create Lead
        Create a new Lead
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/lead'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        
        client = self._security_client
        
        http_res = client.request('POST', url, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.PostCrmLeadResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.PostCrmLeadResponseBody])
                res.response_body = out

        return res

    def details(self, request: operations.GetDetailsCrmLeadRequest) -> operations.GetDetailsCrmLeadResponse:
        r"""Get Lead Details
        Get details about all leads. 
        Details include the type, possible values, and other meta data about the fields.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/lead/details'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetDetailsCrmLeadResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetDetailsCrmLeadResponseBody])
                res.response_body = out

        return res

    def find(self, request: operations.GetOneCrmLeadRequest) -> operations.GetOneCrmLeadResponse:
        r"""Get Lead
        Retrieve a single Lead by Id
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/lead'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetOneCrmLeadResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetOneCrmLeadResponseBody])
                res.response_body = out

        return res

    def list(self, request: operations.GetAllCrmLeadsRequest) -> operations.GetAllCrmLeadsResponse:
        r"""Get All Leads
        Retrieve all leads.
        *CRM Caveats*:
        - Pipedrive: Only `jobTitle` is returned when querying for all leads
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/leads'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetAllCrmLeadsResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetAllCrmLeadsResponseBody])
                res.response_body = out

        return res

    def search(self, request: operations.SearchCrmLeadsRequest) -> operations.SearchCrmLeadsResponse:
        r"""Search Leads
        Search all Leads using filters
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/leads/search'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('POST', url, params=query_params, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.SearchCrmLeadsResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.SearchCrmLeadsResponseBody])
                res.response_body = out

        return res

    def update(self, request: operations.PutCrmLeadRequest) -> operations.PutCrmLeadResponse:
        r"""Update Lead
        Update an existing Lead by Id
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/lead'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        
        client = self._security_client
        
        http_res = client.request('PATCH', url, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.PutCrmLeadResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.PutCrmLeadResponseBody])
                res.response_body = out

        return res

    