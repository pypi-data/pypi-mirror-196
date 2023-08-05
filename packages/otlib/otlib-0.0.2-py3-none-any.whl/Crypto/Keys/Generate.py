from secrets import choice


def key_stream(length, code_charset):
    ks = ""
    for i in range(length):
        ks += choice(code_charset)
    return ks


def key_stream_device(length, device_path, code_charset):
    ks = ""
    with open(device_path, 'rb') as f:
        for i in range(0, length):
            byte = f.read(1)
            num = int.from_bytes(byte, "little")
            ks += code_charset[num % len(code_charset)]
    return ks
