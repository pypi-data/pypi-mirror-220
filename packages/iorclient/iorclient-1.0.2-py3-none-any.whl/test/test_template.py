from ior.iorsdk import IORClient
from ior.util.web3_utils import to_address,keccak256
import unittest


class TestTemplateMethods(unittest.TestCase):
    def setUp(self):
        #main test for example        
        self.ior = IORClient("http://121.5.19.151:8199/tzspace/v1/api")
        self.ior.init_w3()
        self.ior.init_apis()

        self.pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
        self.pk = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

        pub1,pk1 = self.ior.create_account()
        pub2,pk2 = self.ior.create_account()
        pub3,pk3 = self.ior.create_account()

        self.pubs = [self.pub,pub1,pub2,pub3]
        self.pks = {self.pub:self.pk,pub1:pk1,pub2:pk2,pub3:pk3}

    def test_contract(self):
        
        def sign_tx(pub,tx):
            stx = self.ior.sign_transaction(tx,self.pks[pub])
            return stx.rawTransaction.hex()

        pub = self.pubs[0]
        tempctrl = self.ior.get('template')
        contract = self.ior.get('ctrt')

        #初始化模板Id
        tmp_id = 1
        ins_id = 0
        #只需要启动一次
        ret,res = tempctrl.start('tempctrl',pub,sign_tx, tmp_id)
        print('start',res)  

        ret,res = tempctrl.templates('tempctrl',tmp_id)
        print('templates',res)  

        contract_identity = keccak256('测试').hex()

        #注册的结果返回0，需要根据实际结果查看, pub和pk可以是任意用户, 根据模板设计
        ret,ins_id = tempctrl.request_template('tempctrl',pub,sign_tx, tmp_id, contract_identity, 2669296503)
        print('request_template',ret,ins_id)

        ret,res,receipt = contract.init('contract1',pub,sign_tx, ins_id
            , ['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266']
            , '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
            , ['0xb5A3426f9AB8751B868f9492a56A35ccE8a8dBfb','0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266']
            , [8000,2000]
            )
        print('init',res)

        ret,res = contract.verify_hash('contract1', ins_id, contract_identity)
        print('verify_hash',res)

        ret,state = contract.start('contract1',pub,sign_tx, ins_id)
        print('start',state)
        ret,state = contract.sign('contract1',pub,sign_tx, ins_id)
        print('sign',state)
        ret,state = contract.end('contract1',pub,sign_tx, ins_id)
        print('end',state)
        ret,can = contract.can_pay('contract1',ins_id,pub)
        print('can pay',can)
        ret,payees = contract.get_payees('contract1',ins_id)
        print('get_payees',payees)

        for payee in payees:
            _,ratio = contract.get_ratio_by_payee('contract1',ins_id, payee)
            print(payee,ratio)

 
if __name__=='__main__':
    unittest.main()
