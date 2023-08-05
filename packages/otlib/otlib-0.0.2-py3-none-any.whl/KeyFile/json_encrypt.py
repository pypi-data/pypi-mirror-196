from primitives import encrypt, decrypt
import json


def json_encrypt(password, message):
    raw = encrypt(password, message)

    ciphertext, salt = raw

    dicts = {"ciphertext": ciphertext.decode('utf-8'), "salt": salt.decode('utf-8')}
    jsonified = json.dumps(dicts, sort_keys=True, indent=4)
    return jsonified


def json_decrypt(password, jsonified_ciphertext):

    dicts = json.loads(jsonified_ciphertext)
    ciphertext, salt = dicts["ciphertext"], dicts["salt"]
    return decrypt(password, ciphertext, salt)
