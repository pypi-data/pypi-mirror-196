import importlib as _importlib
if __name__ == "__main__":
    import inspect
    import os
    import sys
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../'))


_cipher = "origin"
try:
    from ysc2.utils.rsa import helper as _helper
    _new_cipher = _helper.CIPHER
    if _new_cipher:
        _cipher = _new_cipher
    _cipher_class = _importlib.import_module("ysc2.utils.rsa."+_cipher)
except:
    _cipher = "origin"
    _cipher_class = _importlib.import_module("ysc2.utils.rsa.origin")

rsa_utils = _cipher_class.rsa_utils
generate_rsa_keys = _cipher_class.generate_rsa_keys
__all__ = ["rsa_utils","generate_rsa_keys"]