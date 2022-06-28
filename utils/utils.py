import hashlib


class Utils():

    @staticmethod
    def hash_string(input_str: str):
        return str(int(hashlib.sha256(input_str.encode('utf-8')).hexdigest(), 16) % 10 ** 8)


