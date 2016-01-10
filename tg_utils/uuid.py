import uuid


def get_uuid():
    """ Returns random UUID (uuid4) as hex string.
    """
    return uuid.uuid4().hex
