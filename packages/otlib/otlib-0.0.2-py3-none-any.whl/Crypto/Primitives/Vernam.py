def cipher(msg, key, direction, charset):
    cipher_text = ""
    key = list(key)
    for index, char in enumerate(msg):
        char_index = charset.index(char)
        key_index = charset.index(key[index])
        cipher_code = ((char_index + key_index) if direction is True else (char_index - key_index)) % len(charset)
        cipher_text += charset[cipher_code]
    return cipher_text
