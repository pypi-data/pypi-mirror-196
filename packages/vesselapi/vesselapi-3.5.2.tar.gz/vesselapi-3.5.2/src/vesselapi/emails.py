import requests as requests_http
from . import utils
from typing import Optional
from vesselapi.models import operations

class Emails:
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
        
    def batch(self, request: operations.GetBatchCrmEmailRequest) -> operations.GetBatchCrmEmailResponse:
        r"""Get Batch Emails
        Retrieve Email by a set of Id's
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/email/batch'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetBatchCrmEmailResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetBatchCrmEmailResponseBody])
                res.response_body = out

        return res

    def create(self, request: operations.PostCrmEmailRequest) -> operations.PostCrmEmailResponse:
        r"""Create Email
        Create a new Email.
        *CRM Caveats*:
        
        - Pipedrive: Not supported.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/email'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        
        client = self._security_client
        
        http_res = client.request('POST', url, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.PostCrmEmailResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.PostCrmEmailResponseBody])
                res.response_body = out

        return res

    def details(self, request: operations.GetDetailsCrmEmailRequest) -> operations.GetDetailsCrmEmailResponse:
        r"""Get Email Details
        Get details about all emails. 
        Details include the type, possible values, and other meta data about the fields.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/email/details'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetDetailsCrmEmailResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetDetailsCrmEmailResponseBody])
                res.response_body = out

        return res

    def find(self, request: operations.GetOneCrmEmailRequest) -> operations.GetOneCrmEmailResponse:
        r"""Get Email
        Retrieve a single Task by Id
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/email'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetOneCrmEmailResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetOneCrmEmailResponseBody])
                res.response_body = out

        return res

    def list(self, request: operations.GetAllCrmEmailsRequest) -> operations.GetAllCrmEmailsResponse:
        r"""Get All Emails
        Retrieve all Emails
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/emails'
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('GET', url, params=query_params)
        content_type = http_res.headers.get('Content-Type')

        res = operations.GetAllCrmEmailsResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.GetAllCrmEmailsResponseBody])
                res.response_body = out

        return res

    def search(self, request: operations.SearchCrmEmailsRequest) -> operations.SearchCrmEmailsResponse:
        r"""Search Emails
        Search all Emails using filters
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/emails/search'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        http_res = client.request('POST', url, params=query_params, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.SearchCrmEmailsResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.SearchCrmEmailsResponseBody])
                res.response_body = out

        return res

    def update(self, request: operations.PutCrmEmailRequest) -> operations.PutCrmEmailResponse:
        r"""Update Email
        Update an Email by Id.
        *CRM Caveats*:
        - Pipedrive: Not supported.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix('/') + '/crm/email'
        
        headers = {}
        req_content_type, data, form = utils.serialize_request_body(request)
        if req_content_type not in ('multipart/form-data', 'multipart/mixed'):
            headers['content-type'] = req_content_type
        
        client = self._security_client
        
        http_res = client.request('PATCH', url, data=data, files=form, headers=headers)
        content_type = http_res.headers.get('Content-Type')

        res = operations.PutCrmEmailResponse(status_code=http_res.status_code, content_type=content_type, raw_response=http_res)
        
        if http_res.status_code == 200:
            if utils.match_content_type(content_type, 'application/json'):
                out = utils.unmarshal_json(http_res.text, Optional[operations.PutCrmEmailResponseBody])
                res.response_body = out

        return res

    