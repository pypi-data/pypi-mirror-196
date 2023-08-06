import os
import sys

if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../../'))

from ysc2.utils.ipfs import file as ipfs_file

if __name__ == "__main__":
    import logging
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s"
    )
    logging.debug("[Address][Test] Generate keys for testing")
    from utils import rsa
    pubkey,privkey = rsa.generate_rsa_keys(bits=2048)
    pubkey_cid = ipfs_file.write_to_ipfs(pubkey,cid_version=1)
    account_addr = "YsA" + pubkey_cid[7:]

def get_publickey(address:str)->bytes:
    if not (address.startswith("YsA") or address.startswith("YsG") or address.startswith("YsF") or address.startswith("YsN") or address.startswith("YsD") or address.startswith("Ysd")):
        raise Exception("Invalid address")
    raw_cid = "bafkrei" + address[3:]
    pubkey = ipfs_file.download_from_ipfs(raw_cid)
    ipfs_file.pin_to_ipfs(raw_cid)
    return pubkey

if __name__ == "__main__":
    logging.debug("[Address][Test] Get the public key of account")
    new_pubkey = get_publickey(account_addr)
    try:
        assert new_pubkey == pubkey
    except:
        logging.error("[Address][Test] Get the public key of account failed")
    else:
        logging.debug("[Address][Test] Get the public key of account success")
    

def upload_pubkey(pubkey:bytes,role="user")->str:
    if (not pubkey.startswith(b"-----BEGIN RSA PUBLIC KEY-----")) and role != "bigmulti":
        raise Exception("Invalid pubkey")
    cid = ipfs_file.write_to_ipfs(pubkey,cid_version=1)
    if role in ["user","admin","superadmin","root"]:
        return "YsA" + cid[7:]
    elif role in ["miner_usergroup"]:
        return "YsG" + cid[7:]
    elif role in ["finance"]:
        return "YsF" + cid[7:]
    elif role in ["blackhole"]:
        return "YsN" + cid[7:]
    elif role in ["multi"]:
        return "Ysd" + cid[7:]
    elif role in ["bigmulti"]:
        return "YsD" + cid[7:]
    else:
        return "YsA" + cid[7:]

if __name__ == "__main__":
    logging.debug("[Address][Test] Upload public key to get the address")
    new_address = upload_pubkey(pubkey,role="User")
    try:
        assert new_address == account_addr
    except:
        logging.error("[Address][Test] Upload public key to get the address failed")
    else:
        logging.debug("[Address][Test] Upload public key to get the address success")

def upload_privkey(privkey:bytes):
    if not privkey.startswith(b"-----BEGIN RSA PRIVATE KEY-----"):
        raise Exception("Invalid privkey")
    cid = ipfs_file.write_to_ipfs(privkey,cid_version=1)
    return cid

if __name__ == "__main__":
    logging.debug("[Address][Test] Upload private key to get the address")
    new_address = upload_privkey(privkey)
    
