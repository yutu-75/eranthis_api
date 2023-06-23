import hashlib
import sha3


def md5(text):
    hl = hashlib.md5()
    hl.update(text.encode(encoding='utf-8'))
    return hl.hexdigest()


def keccak_256(text):
    s = sha3.keccak_256()
    s.update(text.encode("utf-8"))
    return s.hexdigest()


def sha256(text):
    data_sha = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return data_sha


if __name__ == "__main__":
    # print(md5("123456789"))
    print(keccak_256("123456789"))
    # print(sha256("asx"))
