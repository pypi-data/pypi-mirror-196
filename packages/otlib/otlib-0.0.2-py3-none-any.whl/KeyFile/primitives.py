import base64

from nacl import pwhash, secret, utils

kdf = pwhash.argon2i.kdf
ops = pwhash.argon2i.OPSLIMIT_SENSITIVE
mem = pwhash.argon2i.MEMLIMIT_SENSITIVE


def encrypt(password, message):
    salt = utils.random(pwhash.argon2i.SALTBYTES)

    key = kdf(secret.SecretBox.KEY_SIZE, bytes(password, 'utf-8'), salt,
              opslimit=ops, memlimit=mem)

    box = secret.SecretBox(key)
    ciphertext = base64.b64encode(box.encrypt(bytes(message, 'utf-8')))
    return ciphertext, base64.b64encode(salt)


def decrypt(password, ciphertext, salt):
    key = kdf(secret.SecretBox.KEY_SIZE, bytes(password, 'utf-8'), base64.b64decode(salt),
              opslimit=ops, memlimit=mem)

    box = secret.SecretBox(key)
    plaintext = box.decrypt(base64.b64decode(ciphertext)).decode('utf-8')
    return plaintext
