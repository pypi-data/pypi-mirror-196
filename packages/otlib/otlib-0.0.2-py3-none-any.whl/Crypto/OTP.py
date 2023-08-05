from Crypto.Primitives import Conversion, Vernam
from Crypto.Keys import Generate


class Create:
    def __init__(self, code_charset, text_charset, padding=True):
        self.conversion_table = Conversion.Table(code_charset, text_charset)
        self.code_charset = code_charset
        self.text_charset = text_charset
        self.padding = padding

    def __otp(self, msg, key, direction, padding):
        if len(msg) == len(key) or (len(key) > len(msg) and padding is False):
            return Vernam.cipher(msg, key, direction, self.code_charset)

        elif len(msg) < len(key) and padding is True:
            n_padding_added = len(key) - len(msg)
            padding_text = Generate.key_stream(n_padding_added, self.code_charset)
            return Vernam.cipher(msg + padding_text, key, direction, self.code_charset)
        elif len(msg) > len(key):
            raise Exception(f"Message is longer than the key by {abs(len(key) - len(msg))} characters, "
                            f"key needs to be equal or greater than message")

    def encrypt(self, msg, key):
        plain_code = self.conversion_table.encode(msg)
        return self.__otp(plain_code, key, True, self.padding)

    def decrypt(self, cipher_text, key):
        plain_code = self.__otp(cipher_text, key, False, self.padding)
        return self.conversion_table.decode(plain_code)
