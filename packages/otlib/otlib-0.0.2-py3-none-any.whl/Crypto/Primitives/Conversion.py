from math import ceil, pow


def extract_characters(string):
    old = list(string)
    new = []
    for i in range(len(old)):
        if ord(old[i]) != 65039:
            new.append(old[i])
    return new


class Table:
    def __init__(self, code_charset, text_charset):
        self.conversion_table = self.__generate(code_charset, text_charset)

    @staticmethod
    def __generate(code_charset, text_charset):
        conversion_table = dict()

        max_encode_len = ceil(len(text_charset) / len(code_charset))
        space_reserved = len(code_charset) * max_encode_len
        space_left = pow(len(code_charset), 2)
        has_initialised = False

        if space_reserved > space_left:
            msg = """You reserved {0} space, maximum of {1} is allowed
            Try increasing the amount of characters in the codeCharset"""
            raise AttributeError(msg.format(space_reserved, space_left))

        j, k = 0, 0
        for text_charset_index in range(0, len(text_charset)):
            if (space_left - len(code_charset)) > space_reserved:
                conversion_table[code_charset[text_charset_index]] = text_charset[text_charset_index]
                space_left = (len(code_charset) - text_charset_index) * len(code_charset)
            else:
                if not has_initialised:
                    k = text_charset_index
                    has_initialised = True

                key = code_charset[k] + code_charset[j]
                conversion_table[key] = text_charset[text_charset_index]
                space_left -= 1
                j += 1

                if j >= len(code_charset):
                    j = 0
                    k += 1

        return conversion_table

    def encode(self, msg):
        trans = ""
        conversion_table = dict(zip(self.conversion_table.values(), self.conversion_table.keys()))
        for item in extract_characters(msg):
            trans += conversion_table[item]
        return trans

    def decode(self, code):
        trans, two_string = "", ""
        code_lst = extract_characters(code)
        i = 0
        while i < len(code_lst):
            if i < len(code_lst) - 1 and code_lst[i] not in self.conversion_table:
                two_string = code_lst[i] + code_lst[i + 1]
            if code_lst[i] in self.conversion_table:
                trans += self.conversion_table[code_lst[i]]
            elif two_string in self.conversion_table:
                trans += self.conversion_table[two_string]
                i += 1
            i += 1
        return trans
