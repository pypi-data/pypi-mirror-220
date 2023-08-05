from ior.iorsdk import IORClient
import unittest

class TestCertMethods(unittest.TestCase):
    def test_cert(self):
        #main test for example
        
        ior = IORClient("http://127.0.0.1:5000/v1/api")
        ior.init_w3()
        ior.init_apis()

        pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
        pk = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

        pub1,pk1 = ior.create_account()
        pub2,pk2 = ior.create_account()
        pub3,pk3 = ior.create_account()

        self.pks = {pub:pk,pub1:pk1,pub2:pk2,pub3:pk3}
        def sign_tx(pub,tx):
            stx = ior.sign_transaction(tx,self.pks[pub])
            return stx.rawTransaction.hex()

        certId = ior.get('cert').mint('stcc',pub,sign_tx, pub)
        print(certId)


 
if __name__=='__main__':
    unittest.main()
