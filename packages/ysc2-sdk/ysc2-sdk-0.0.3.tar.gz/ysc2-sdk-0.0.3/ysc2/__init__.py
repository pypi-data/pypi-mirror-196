import json
import os
import time
import requests
import base64

from ysc2.utils import rsa
from ysc2.utils.rsa import trade as trade_tools
from ysc2.utils.rsa import mutrades as mutrades_tools
from ysc2.utils.ipfs import file as ipfs_file
from ysc2.utils.ipfs import addresses as ipfs_addresses



class ysc:
    def __init__(self,address,privatekey,ysc_gateway_url):
        self.address = address
        self.publickey_str = ipfs_addresses.get_publickey(address)
        self.privatekey = privatekey
        if self.privatekey.startswith("bafkrei"):
            self.privatekey = ipfs_file.download_from_ipfs(self.privatekey)
        self.ysc_gateway_url = ysc_gateway_url
        self.signer = trade_tools.trade_signer(self.publickey_str,self.privatekey)
        r = self.getuserinfo()



    @staticmethod
    def settimezone(timezone):
        os.environ['TZ'] = timezone
        time.tzset()

    def getuserinfo(self):
        url = self.ysc_gateway_url + "/api/v1/getuserinfo"
        data = {"uid":self.address}
        r = requests.post(url,data=data,verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        self.role = ret["role"]
        self.balance = ret["balance"]
        return ret
    
    def getbalance(self):
        url = self.ysc_gateway_url + "/api/v1/getbalance"
        data = {"uid":self.address}
        r = requests.post(url,data=data,verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        self.balance = ret["balance"]
        return ret["balance"]
        
    def getheadblock(self):
        url = self.ysc_gateway_url + "/api/v1/getheadblock"
        r = requests.get(url,verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret
    
    def getblock(self,cid):
        url = self.ysc_gateway_url + "/api/v1/getblock"
        r = requests.get(url,data={"cid":cid},verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret

    def gettrade(self,cid,offset):
        url = self.ysc_gateway_url + "/api/v1/gettrade"
        r = requests.post(url,data={"cid":cid,"offset":offset},verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret

    def getusertrade(self,depth=20):
        url = self.ysc_gateway_url + "/api/v1/getusertrade"
        r = requests.post(url,data={"uid":self.address,"depth":depth},verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret

    def createdeal(self,to,value,transfer_type="Send",content={"cipher":None,"msg":"Transfer"},tax=0,strict_waiting = False):
        transfer = {
            "from": self.address,
            "to": to,
            "type":transfer_type,
            "timestamp":int(time.time()),
            "tax":int(abs(tax)),
            "value":int(value),
            "content":content
        }
        
        signed_transfer = self.signer.sign_trade(transfer)
        json_transfer = json.dumps(signed_transfer)

        r = requests.post(self.ysc_gateway_url+"/api/v1/createdeal",data={"data":str(base64.b64encode(json_transfer.encode()),'utf-8')},verify=False)
        output = r.json()
        if strict_waiting:
            now_block = self.getheadblock()
            if now_block["status"] == False:
                raise Exception(now_block["msg"])
            now_block = now_block["data"]["block"]
            for i in range(0,15):
                time.sleep(10)
                new_block = self.getheadblock()
                if new_block["status"] == False:
                    raise Exception(now_block["msg"])
                new_block_data = new_block["data"]["data"]
                new_block = new_block["data"]["block"]
                if new_block == now_block:
                    continue
                offset = 0
                for j in new_block_data["transfers"]:
                    raw_data = json.loads(base64.b64decode(j["raw_trade"].encode()))
                    if raw_data["sign"] == signed_transfer["sign"]:
                        if j["status"] == 1:
                            return{
                                "status":True,
                                "msg":"success",
                                "block_cid":new_block+"|"+str(offset)
                            }
                        else:
                            return{
                                "status":False,
                                "msg":j["content"]["msg"]
                            }
                    offset+=1
                now_block = new_block
            return{
                "status":False,
                "msg":"timeout"
            }

        if output["status"] == False:
            raise Exception("Create Deal Failed: "+output["msg"])
        else:
            return output

    def createuser(self,rsa_bits=4096,role="user",tax=0,strict_waiting = False):

        newkeys = rsa.generate_rsa_keys(rsa_bits)
        publickey = newkeys[0]
        privatekey = newkeys[1]
        new_publickey_cid = ipfs_file.write_to_ipfs(str(publickey,'utf-8'),cid_version=1)
        new_privatekey_cid = ipfs_file.write_to_ipfs(str(privatekey,'utf-8'),cid_version=1)
        address = ipfs_addresses.upload_pubkey(publickey,role=role)
        msg = str(base64.b64encode(json.dumps({"publickey":new_publickey_cid,"role":role}).encode()),'utf-8')
        transfer = {
            "from": self.address,
            "to": address,
            "type":"AddUser",
            "timestamp":int(time.time()),
            "tax":int(abs(tax)),
            "value":0,
            "content":{
                "cipher":None,
                "msg":msg
            }
        }
        signed_transfer = self.signer.sign_trade(transfer)
        json_transfer = json.dumps(signed_transfer)

        r = requests.post(self.ysc_gateway_url+"/api/v1/createuser",data={"data":str(base64.b64encode(json_transfer.encode()),'utf-8')},verify=False)
        output = r.json()

        if strict_waiting:
            now_block = self.getheadblock()
            if now_block["status"] == False:
                raise Exception(now_block["msg"])
            now_block = now_block["data"]["block"]
            for i in range(0,15):
                time.sleep(10)
                new_block = self.getheadblock()
                if new_block["status"] == False:
                    raise Exception(now_block["msg"])
                new_block_data = new_block["data"]["data"]
                new_block = new_block["data"]["block"]
                if new_block == now_block:
                    continue
                offset = 0
                for j in new_block_data["transfers"]:
                    raw_data = json.loads(base64.b64decode(j["raw_trade"].encode()))

                    if raw_data["sign"] == signed_transfer["sign"]:
                        if j["status"] == 1:
                            return{
                                "status":True,
                                "msg":"success",
                                "block_cid":new_block+"|"+str(offset),
                                "publickey":new_publickey_cid,
                                "privatekey":new_privatekey_cid,
                            }
                        else:
                            return{
                                "status":False,
                                "msg":j["content"]["msg"],
                                "publickey":new_publickey_cid,
                                "privatekey":new_privatekey_cid,
                            }
                    offset+=1
            return{
                "status":False,
                "msg":"timeout",
                "publickey":new_publickey_cid,
                "privatekey":new_privatekey_cid,
                "address":address
            }

        if output["status"] == False:
            raise Exception("Create Account Failed: "+output["msg"])
        else:
            return {
                "publickey":new_publickey_cid,
                "privatekey":new_privatekey_cid,
                "address":address
            }     
class muysc:
    def __init__(self,address,privatekey,ysc_gateway_url):
        self.address = address
        self.publickey_str = ipfs_addresses.get_publickey(address)
        self.privatekey = privatekey
        if self.privatekey.startswith("bafkrei"):
            self.privatekey = ipfs_file.download_from_ipfs(self.privatekey)
        self.ysc_gateway_url = ysc_gateway_url
        self.signer = mutrades_tools.trade_signer(self.address,self.privatekey)
        self.verfier = mutrades_tools.trade_verify(self.address)
        r = self.getuserinfo()



    @staticmethod
    def settimezone(timezone):
        os.environ['TZ'] = timezone
        time.tzset()

    def getuserinfo(self):
        url = self.ysc_gateway_url + "/api/v1/getuserinfo"
        data = {"uid":self.address}
        r = requests.post(url,data=data,verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        self.role = ret["role"]
        self.balance = ret["balance"]
        return ret
    
    def getbalance(self):
        url = self.ysc_gateway_url + "/api/v1/getbalance"
        data = {"uid":self.address}
        r = requests.post(url,data=data,verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        self.balance = ret["balance"]
        return ret["balance"]
        
    def getheadblock(self):
        url = self.ysc_gateway_url + "/api/v1/getheadblock"
        r = requests.get(url,verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret
    
    def getblock(self,cid):
        url = self.ysc_gateway_url + "/api/v1/getblock"
        r = requests.get(url,data={"cid":cid},verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret

    def gettrade(self,cid,offset):
        url = self.ysc_gateway_url + "/api/v1/gettrade"
        r = requests.post(url,data={"cid":cid,"offset":offset},verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret

    def getusertrade(self,depth=20):
        url = self.ysc_gateway_url + "/api/v1/getusertrade"
        r = requests.post(url,data={"uid":self.address,"depth":depth},verify=False)
        ret = r.json()
        if ret["status"] == False:
            raise Exception(ret["msg"])
        return ret

    def createdeal(self,to,value,transfer_type="Send",content={"cipher":None,"msg":"Transfer"},tax=0)->str:
        transfer = {
            "from": self.address,
            "to": to,
            "type":transfer_type,
            "timestamp":int(time.time()),
            "tax":int(abs(tax)),
            "value":int(value),
            "content":content
        }
        signed_transfer = self.signer.sign_trade(transfer)
        return {
            "b64trade":str(base64.b64encode(json.dumps(signed_transfer).encode()),'utf-8')
        }
    
    def createuser(self,rsa_bits=4096,role="user",tax=0,strict_waiting = False)->dict:

        newkeys = rsa.generate_rsa_keys(rsa_bits)
        publickey = newkeys[0]
        privatekey = newkeys[1]
        new_publickey_cid = ipfs_file.write_to_ipfs(str(publickey,'utf-8'),cid_version=1)
        new_privatekey_cid = ipfs_file.write_to_ipfs(str(privatekey,'utf-8'),cid_version=1)
        address = ipfs_addresses.upload_pubkey(publickey,role=role)
        msg = str(base64.b64encode(json.dumps({"publickey":new_publickey_cid,"role":role}).encode()),'utf-8')
        transfer = {
            "from": self.address,
            "to": address,
            "type":"AddUser",
            "timestamp":int(time.time()),
            "tax":int(abs(tax)),
            "value":0,
            "content":{
                "cipher":None,
                "msg":msg
            }
        }
        signed_transfer = self.signer.sign_trade(transfer)
        return {
                "publickey":new_publickey_cid,
                "privatekey_cid":new_privatekey_cid,
                "privatekey":str(privatekey,'utf-8'),
                "address":address,
                "b64trade":str(base64.b64encode(json.dumps(signed_transfer).encode()),'utf-8')
            }

    def sign_transfer(self,b64transfer:str)->str:
        transfer = json.loads(base64.b64decode(b64transfer).decode())
        signed_transfer = self.signer.sign_trade(transfer)
        return str(base64.b64encode(json.dumps(signed_transfer).encode()),'utf-8')

    def merge_sign_transfer(self,b64transfer1:str,b64transfer2:str)->str:
        transfer1 = json.loads(base64.b64decode(b64transfer1).decode())
        transfer2 = json.loads(base64.b64decode(b64transfer2).decode())
        signed_transfer = self.signer.merge_trade(transfer1,transfer2)
        return str(base64.b64encode(json.dumps(signed_transfer).encode()),'utf-8')
    
    def makerequest(self,b64transfer:str,strict_waiting = False):
        signed_transfer = json.loads(base64.b64decode(b64transfer).decode())
        r = requests.post(self.ysc_gateway_url+"/api/v1/createdeal",data={"data":b64transfer},verify=False)
        output = r.json()
        if strict_waiting:
            now_block = self.getheadblock()
            if now_block["status"] == False:
                raise Exception(now_block["msg"])
            now_block = now_block["data"]["block"]
            for i in range(0,15):
                time.sleep(10)
                new_block = self.getheadblock()
                if new_block["status"] == False:
                    raise Exception(now_block["msg"])
                new_block_data = new_block["data"]["data"]
                new_block = new_block["data"]["block"]
                if new_block == now_block:
                    continue
                offset = 0
                for j in new_block_data["transfers"]:
                    raw_data = json.loads(base64.b64decode(j["raw_trade"].encode()))
                    if raw_data["sign"] == signed_transfer["sign"]:
                        if j["status"] == 1:
                            return{
                                "status":True,
                                "msg":"success",
                                "block_cid":new_block+"|"+str(offset)
                            }
                        else:
                            return{
                                "status":False,
                                "msg":j["content"]["msg"]
                            }
                    offset+=1
                now_block = new_block
            return{
                "status":False,
                "msg":"timeout"
            }

        if output["status"] == False:
            raise Exception("Create Deal Failed: "+output["msg"])
        else:
            return output

    
__all__ = ["ysc","muysc"]