import os
import sys
import json
import logging
import base64


if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../'))

from ysc2.utils import rsa
from ysc2.utils.ipfs import addresses as ipfs_addresses

def gen_address(bits=2048,num=61):
    addresses = []
    addresses_t = []
    for i in range(num):
        newkeys = rsa.generate_rsa_keys(bits=bits)
        addresses.append(newkeys)
        addresses_t.append(ipfs_addresses.upload_pubkey(newkeys[0],role="multi"))
    raw_address_content = "\n".join(addresses_t)
    raw_address_cid = ipfs_addresses.upload_pubkey(raw_address_content.encode(),role="bigmulti")
    return {
        "address":raw_address_cid,
        "contents":addresses
    }
if __name__ == "__main__":
    new_addresses = gen_address()
class trade_signer():
    def __init__(self,addresses,privatekey):
        self.addresses = addresses # Main Address
        naddress = str(ipfs_addresses.get_publickey(addresses),encoding="utf-8")
        self.naddress = naddress.split("\n") # Each publickey's address
        self.paddress = {} # Each publickey's content
        self.publickeys = {} # Each publickey's library
        self.nprivatekey = privatekey # One privatekey's content
        self.pprivatekey = rsa.rsa_utils(prikey=privatekey) # One privatekey's library
        self.privatekey_from = None # One privatekey's address
        for address in self.naddress:
            paddress = ipfs_addresses.get_publickey(address)
            self.paddress[address] = paddress
            self.publickeys[address] = rsa.rsa_utils(pubkey=paddress)
            if self.publickeys[address].verify(b"Hello",self.pprivatekey.sign(b"Hello")):
                self.privatekey_from = address
                self.publickeys[address] = rsa.rsa_utils(pubkey=paddress,prikey=privatekey)
        if self.privatekey_from is None:
            raise Exception("No privatekey matched")
    def sign_trade(self,trade:dict):
        if "sign" in trade:
            org_sign = trade["sign"]
            org_sign_data = json.loads(base64.b64decode(org_sign))
            del trade["sign"]
        else:
            org_sign_data = {}
        sorted_trade = dict(sorted(trade.items(), key=lambda x: x[0],reverse=False))
        encoded_trade = json.dumps(sorted_trade)
        for addr in org_sign_data:
            if addr not in self.naddress:
                raise Exception("No address matched")
            sign_val = org_sign_data[addr]
            if not self.publickeys[addr].verify(encoded_trade.encode(),base64.b64decode(sign_val)):
                raise Exception("Sign not matched")
        signed_trade = base64.b64encode(self.publickeys[self.privatekey_from].sign(encoded_trade.encode()))
        org_sign_data[self.privatekey_from] = str(signed_trade,encoding="utf-8")
        trade["sign"] = str(base64.b64encode(json.dumps(org_sign_data).encode()),encoding="utf-8")
        return trade
    def merge_trade(self,trade1:dict,trade2:dict):
        if "sign" not in trade1 or "sign" not in trade2:
            raise Exception("No sign in trade")
        org_sign1 = trade1["sign"]
        org_sign_data1 = json.loads(base64.b64decode(org_sign1))
        org_sign2 = trade2["sign"]
        org_sign_data2 = json.loads(base64.b64decode(org_sign2))
        del trade1["sign"]
        del trade2["sign"]
        sorted_trade1 = dict(sorted(trade1.items(), key=lambda x: x[0],reverse=False))
        sorted_trade2 = dict(sorted(trade2.items(), key=lambda x: x[0],reverse=False))
        encoded_trade1 = json.dumps(sorted_trade1)
        encoded_trade2 = json.dumps(sorted_trade2)
        if encoded_trade1 != encoded_trade2:
            raise Exception("Trade not match")
        merge_sign_data = {}
        merge_sign_data.update(org_sign_data1)
        merge_sign_data.update(org_sign_data2)
        merge_sign = base64.b64encode(json.dumps(merge_sign_data).encode())
        trade1["sign"] = str(merge_sign,encoding="utf-8")
        return self.sign_trade(trade1)
        

if __name__ == "__main__":
    original_trade = {
        "from":new_addresses["address"],
        "to":new_addresses["address"],
        "value":1,
        "content":{
            "cipher":None,
            "msg":"Hello"
        },
        "tax":0
    }
    original_trade2 = original_trade.copy()
    signer = []
    for addr in new_addresses["contents"][0:len(new_addresses["contents"])//4+2]:
        signer.append(trade_signer(new_addresses["address"],addr[1]))
        original_trade = signer[-1].sign_trade(original_trade)
    for addr in new_addresses["contents"][len(new_addresses["contents"])//2:len(new_addresses["contents"])//4*3+2]:
        signer.append(trade_signer(new_addresses["address"],addr[1]))
        original_trade2 = signer[-1].sign_trade(original_trade2)
    final_signer = trade_signer(new_addresses["address"],new_addresses["contents"][-1][1])
    final_trade = final_signer.merge_trade(original_trade,original_trade2)
    #signer = trade_signer(new_addresses["address"],new_addresses["contents"][0][1])
    print(json.dumps(final_trade,indent=4))

class trade_verify():
    def __init__(self,addresses):
        self.addresses = addresses # Main Address
        naddress = str(ipfs_addresses.get_publickey(addresses),encoding="utf-8")
        self.naddress = naddress.split("\n") # Each publickey's address
        self.paddress = {} # Each publickey's content
        self.publickeys = {} # Each publickey's library
        for address in self.naddress:
            paddress = ipfs_addresses.get_publickey(address)
            self.paddress[address] = paddress
            self.publickeys[address] = rsa.rsa_utils(pubkey=paddress)

    def verify_trade(self,trade:dict)->bool:
        new_trade = trade.copy()
        sign_message = new_trade["sign"]
        sign_message = base64.b64decode(sign_message)
        del new_trade["sign"]
        sorted_trade = dict(sorted(new_trade.items(), key=lambda x: x[0],reverse=False))
        encoded_trade = json.dumps(sorted_trade)
        len_addrs = len(self.naddress)
        num_of_verify = 0
        org_sign_data = json.loads(sign_message)
        for address in org_sign_data:
            if address in self.naddress:
                if self.publickeys[address].verify(encoded_trade.encode(),base64.b64decode(org_sign_data[address])):
                    num_of_verify += 1
        if num_of_verify > len_addrs//2:
            return True
        else:
            return False

if __name__ == "__main__":
    verify = trade_verify(new_addresses["address"])
    if verify.verify_trade(final_trade):
        print("Trade verified")