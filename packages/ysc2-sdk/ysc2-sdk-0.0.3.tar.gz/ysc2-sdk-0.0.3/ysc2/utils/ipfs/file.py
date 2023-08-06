import os
import sys

if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../../'))


import requests
import json
import logging
import re
from threading import Thread
from ysc2.utils.ipfs import apihelper

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s"
    )

def write_to_ipfs(string:str,cid_version=1)->str:
    """
    Write the string to ipfs and return its CID.
    """
    ret = requests.post(url=apihelper.IPFS_API+"/api/v0/add?pin=true&cid-version="+str(cid_version),files={'file':string})
    cid = ret.json()["Hash"]
    return cid

if __name__ == "__main__":
    logging.debug("[IPFS][Test] Testing IPFS")
    test_cid = write_to_ipfs("hello world")

def load_from_ipfs(cid:str)->str:
    """
    Load the content of the cid from ipfs.
    """
    if not re.match("Qm[1-9A-HJ-NP-Za-km-z]{44,}|b[A-Za-z2-7]{58,}|B[A-Z2-7]{58,}|z[1-9A-HJ-NP-Za-km-z]{48,}|F[0-9A-F]{50,}",cid):
        raise Exception("Invalid cid")
    res = requests.get(url=apihelper.IPFS_GW+"/ipfs/"+cid,timeout=60)
    if res.status_code != 200:
        raise Exception("load from IPFS failed")
    return res.text

if __name__ == "__main__":
    test_str = load_from_ipfs(test_cid)
    try:
        assert test_str == "hello world"
    except:
        logging.error("[IPFS][Test] Load String failed")
    else:
        logging.debug("[IPFS][Test] Load String passed")

def download_from_ipfs(cid:str)->bytes:
    """
    Load the content of the cid from ipfs.
    """
    if not re.match("Qm[1-9A-HJ-NP-Za-km-z]{44,}|b[A-Za-z2-7]{58,}|B[A-Z2-7]{58,}|z[1-9A-HJ-NP-Za-km-z]{48,}|F[0-9A-F]{50,}",cid):
        raise Exception("Invalid cid")
    res = requests.get(url=apihelper.IPFS_GW+"/ipfs/"+cid,timeout=60)
    if res.status_code != 200:
        raise Exception("Download failed")
    return res.content

if __name__ == "__main__":
    test_str = download_from_ipfs(test_cid)
    try:
        assert test_str == b"hello world"
    except:
        logging.error("[IPFS][Test] Download failed")
    else:
        logging.debug("[IPFS][Test] Download passed")
    
class pin_to_ipfs(Thread):
    def __init__(self,cid:str,is_background=False):
        Thread.__init__(self)
        self.cid = cid
        self.is_background = is_background
        self.start()
        if not self.is_background:
            self.join()
    def run(self):
        cid = self.cid
        if not re.match("Qm[1-9A-HJ-NP-Za-km-z]{44,}|b[A-Za-z2-7]{58,}|B[A-Z2-7]{58,}|z[1-9A-HJ-NP-Za-km-z]{48,}|F[0-9A-F]{50,}",cid):
            raise Exception("Invalid cid")
        res = requests.post(url=apihelper.IPFS_API+"/api/v0/pin/add?arg="+self.cid,timeout=60)
        if res.status_code != 200:
            logging.error("[IPFS][PIN] Pinning {cid} is Failed, The Response is {res}".format(cid=self.cid,res=res.text))
        else:
            logging.info("[IPFS][PIN] Pinning {cid} is Success".format(cid=self.cid))
        return