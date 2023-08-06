from ..util.result_utils import error_handler,two_ret_error_handler
from rest_api_client.lib import (
    RestAPI,
    Endpoint,
    HTTPMethod,
    MissingMethodName,
    BearerHeaderToken,
)

class CertificateService(object):
    def __init__(self):
        None

    def set_api_client(self, server_url, client):
        self._api = RestAPI(api_url=server_url+"/certificate" ,driver=client)
        endpoints = [
            Endpoint(name="address",path="/get_address",method=HTTPMethod.POST),
            Endpoint(name="pretokens",path="/get_preTokenById",method=HTTPMethod.POST),
            Endpoint(name="recreations",path="/get_recreationById",method=HTTPMethod.POST),
            Endpoint(name="isApproved",path="/is_authorizeApproved",method=HTTPMethod.POST),
            Endpoint(name="tokenUri",path="/get_tokenUri",method=HTTPMethod.POST),
            Endpoint(name="verifyOwner",path="/verify_owner",method=HTTPMethod.POST),
            Endpoint(name="verifyHash",path="/verify_hash",method=HTTPMethod.POST),
            Endpoint(name="updateHash",path="/estimate_updateHash_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="updateBaseUri",path="/estimate_updateBaseUri_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="setAuthorizeApproval",path="/estimate_setAuthorizeApproval_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="bindOption",path="/estimate_bindOption_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="setApproveForAll",path="/estimate_setApproveForAll_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="approve",path="/estimate_approve_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="recreateCrossChain",path="/prepare_recreateCrossChain_forResult",method=HTTPMethod.POST),
            Endpoint(name="recreateInChain",path="/prepare_recreateInChain_forResult",method=HTTPMethod.POST),
            Endpoint(name="recreate",path="/prepare_recreate_forResult",method=HTTPMethod.POST),
            Endpoint(name="authorizeOption",path="/prepare_authorizeOption_forResult",method=HTTPMethod.POST),
            Endpoint(name="createOption",path="/prepare_createOption_forResult",method=HTTPMethod.POST),
            Endpoint(name="authorize",path="/prepare_authorize_forResult",method=HTTPMethod.POST),
            Endpoint(name="safeTransferFrom",path="/prepare_safeTransferFrom_forResult",method=HTTPMethod.POST),
            Endpoint(name="mint",path="/prepare_mint_forResult",method=HTTPMethod.POST),
            Endpoint(name="tryForReceipt",path="/try_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="tryForResult",path="/try_forResult",method=HTTPMethod.POST),
        ]
        self._api.register_endpoints(endpoints)

    @error_handler
    def address(self, service_name):
        res = self._api.call_endpoint("address",data=
            {
                'name': service_name
            })
        return res['data']

    @error_handler
    def pretokens(self, service_name, _certId):
        res = self._api.call_endpoint("pretokens",data=
            {
                'name': service_name, 
                'certId': _certId
            })
        return res['data']

    @error_handler
    def recreations(self, service_name, _certId):
        res = self._api.call_endpoint("recreations",data=
            {
                'name': service_name, 
                'certId': _certId
            })
        return res['data']

    @error_handler
    def is_authorize_approved(self, service_name,  _certId, _to):
        res = self._api.call_endpoint("isApproved",data=
            {
                'name': service_name, 
                'certId': _certId, 
                'to': _to
            })
        return res['data']

    @error_handler
    def token_uri(self, certId: int):
        res = self._api.call_endpoint("tokenUri",data=
            {
                'name': service_name, 
                'certId': _certId, 
                'sender': pub
            })
        return res['data']

    @error_handler
    def verify_owner(self, service_name, _certId, _to):
        res = self._api.call_endpoint("verifyOwner",data=
            {
                'name': service_name, 
                'certId': _certId, 
                'to': _to
            })
        return res['data']


    @error_handler
    def verify_hash(self, service_name, _certId, _hash):
        res = self._api.call_endpoint("verifyHash",data=
            {
                'name': service_name, 
                'certId': _certId, 
                'hash': _hash
            })
        return res['data']

    @two_ret_error_handler
    def update_hash(self, service_name, pub, sign_func,  _certId,_hash):
        res = self._api.call_endpoint("updateHash",data=
            {
                'name': service_name, 
                'certId': _certId, 
                'hash': _hash, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

    @two_ret_error_handler
    def update_base_uri(self, service_name, pub, sign_func,  _uri):
        res = self._api.call_endpoint("updateBaseUri",data=
            {
                'name': service_name, 
                'uri': _uri, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

    @two_ret_error_handler
    def set_authorize_approval(self, service_name, pub, sign_func,  _certId,_to,_approved):
        res = self._api.call_endpoint("setAuthorizeApproval",data=
            {
                'name': service_name, 
                'certId': _certId, 
                'to': _to, 
                'approved': _approved, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

    @two_ret_error_handler
    def bind_option(self, service_name, pub, sign_func,  _option):
        res = self._api.call_endpoint("bindOption",data=
            {
                'name': service_name, 
                'option': _option, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

    @two_ret_error_handler
    def set_approve_for_all(self, service_name, pub, sign_func,  _to,_approved):
        res = self._api.call_endpoint("setApproveForAll",data=
            {
                'name': service_name, 
                'to': _to, 
                'approved': _approved, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

    @error_handler
    def approve(self, service_name, pub, sign_func,  _to,_certId):
        res = self._api.call_endpoint("approve",data=
            {
                'name': service_name, 
                'to': _to, 
                'certId': _certId, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForResult",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    @error_handler
    def recreate_cross_chain(self, service_name, pub, sign_func,   _to,_chains,_certs,_certIds):
        res = self._api.call_endpoint("recreateCrossChain",data=
            {
                'name': service_name, 
                'to': _to, 
                'chains': _chains, 
                'certs': _certs, 
                'certIds': _certIds, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForResult",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    @error_handler
    def recreate_in_chain(self, service_name, pub, sign_func,  _to,_certs,_certIds):
        res = self._api.call_endpoint("recreateInChain",data=
            {
                'name': service_name, 
                'to': _to, 
                'certs': _certs, 
                'certIds': _certIds, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForResult",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    @error_handler
    def recreate(self, service_name, pub, sign_func,   _to,_certIds):
        res = self._api.call_endpoint("recreate",data=
            {
                'name': service_name, 
                'to': _to, 
                'certIds': _certIds, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForResult",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    @error_handler
    def authorize_option(self, service_name, pub, sign_func,  _to,_certId,_optionId):
        res = self._api.call_endpoint("authorizeOption",data=
            {
                'name': service_name, 
                'to': _to, 
                'certId': _certId, 
                '_optionId': _optionId, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForResult",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    def create_option(self, service_name, pub, sign_func,  _to,_certId,_price,_effectDate):
        res = self._api.call_endpoint("createOption",data=
            {
                'name': service_name, 
                'to': _to, 
                'certId': _certId, 
                'price': _price, 
                'effectDate': _effectDate, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForResult",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    @error_handler
    def authorize(self, service_name, pub, sign_func,  _to,_certId):
        res = self._api.call_endpoint("authorize",data=
            {
                'name': service_name, 
                'to': _to, 
                'certId': _certId, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForResult",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    @error_handler
    def safe_transfer_from(self, service_name, pub, sign_func,  _from,_to,_certId):
        res = self._api.call_endpoint("safeTransferFrom",data=
            {
                'name': service_name, 
                'from': _from, 
                'to': _to, 
                'certId': _certId, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForResult",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

    @error_handler
    def mint(self, service_name, pub, sign_func,  _to):
        res = self._api.call_endpoint("mint",data=
            {
                'name': service_name, 
                'to': _to, 
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForResult",data={'name': service_name, 'tx': raw})
        res = result['data']['res']
        return res

