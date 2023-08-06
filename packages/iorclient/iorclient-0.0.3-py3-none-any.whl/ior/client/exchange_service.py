from ..util.result_utils import error_handler,two_ret_error_handler
from rest_api_client.lib import (
    RestAPI,
    Endpoint,
    HTTPMethod,
    MissingMethodName,
    BearerHeaderToken,
)

class ExchangeService(object):
    def __init__(self):
        None

    def set_api_client(self, server_url, client):
        self._api = RestAPI(api_url=server_url+"/exchange" ,driver=client)
        endpoints = [
            Endpoint(name="address",path="/get_address",method=HTTPMethod.POST),
            Endpoint(name="exchange",path="/estimate_exchange_forReceipt",method=HTTPMethod.POST),
            Endpoint(name="exchangeWithFeed",path="/estimate_exchangeWithFeed_forReceipt",method=HTTPMethod.POST),
        ]
        self._api.register_endpoints(endpoints)

    @error_handler
    def address(self, service_name):
        res = self._api.call_endpoint("address",data=
            {
                'name': service_name
            })
        return res['data']
        
    @two_ret_error_handler
    def exchange(self, service_name, pub, sign_func,  _certAddress, _certId, _from, _to, _price):
        res = self._api.call_endpoint("exchange",data=
            {
                'name': service_name, 
                'certAddress': _certAddress, 
                'certId': _certId, 
                'from': _from,
                'to': _to,
                'price': _price,
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']


    @two_ret_error_handler
    def exchange_with_feed(self, service_name, pub, sign_func,  
            _certAddress, _certId, _from, _to, _fee, _feeds, _percents):

        res = self._api.call_endpoint("exchangeWithFeed",data=
            {
                'name': service_name, 
                'certAddress': _certAddress, 
                'certId': _certId, 
                'from': _from,
                'to': _to,
                'fee': _fee,
                'feeds': _feeds,
                'percents': _percents,
                'sender': pub
            })
        tx = res['data']['transaction']

        raw = sign_func(pub, tx)
        result = self._api.call_endpoint("tryForReceipt",data={'name': service_name, 'tx': raw})
        return result['data']['code'],result['data']['receipt']

