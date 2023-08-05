from json_encrypt import json_decrypt, json_encrypt
import json


def save_keys(password, keys, path):
    ciphertext = json_encrypt(password, json.dumps({"keys": keys}))
    with open(path, 'w') as f:
        f.write(ciphertext)


def load_keys(password, path):
    with open(path, 'r') as f:
        json_ciphertext = f.read()
    plaintext = json.loads(json_decrypt(password, json_ciphertext))
    return plaintext["keys"]


def change_keys_password(old_pass, new_pass, path):
    keys = load_keys(old_pass, path)
    save_keys(new_pass, keys, path)


def use_key(password, path):
    keys = load_keys(password, path)
    key = keys.pop(0)
    save_keys(password, keys, path)
    return key
