import uuid


def get_new_uuid():
    return str(uuid.uuid4())


if __name__ == '__main__':
    print(get_new_uuid())
    print(uuid.uuid4())
