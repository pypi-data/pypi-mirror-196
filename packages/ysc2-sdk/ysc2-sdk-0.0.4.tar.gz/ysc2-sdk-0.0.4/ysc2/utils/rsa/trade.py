from ysc2.utils import rsa
import os
import sys
import json
import logging
import base64

class trade_signer(rsa.rsa_utils):
    def __init__(self,*args,**kwargs):
        rsa.rsa_utils.__init__(self,*args,**kwargs)
    
    def sign_trade(self,trade:dict)->dict:
        sorted_trade = dict(sorted(trade.items(), key=lambda x: x[0],reverse=False))
        encoded_trade = json.dumps(sorted_trade)
        signed_trade = base64.b64encode(self.sign(encoded_trade.encode()))
        trade["sign"] = str(signed_trade,encoding="utf-8")
        return trade

    def verify_trade(self,trade:dict)->bool:
        new_trade = trade.copy()
        sign_message = new_trade["sign"]
        sign_message = base64.b64decode(sign_message)
        del new_trade["sign"]
        sorted_trade = dict(sorted(new_trade.items(), key=lambda x: x[0],reverse=False))
        encoded_trade = json.dumps(sorted_trade)
        return self.verify(encoded_trade.encode(),sign_message)