import msgpack
from cramjam import zstd


def deserialize(data):
    if data is None:
        return None
    return msgpack.unpackb(bytes(zstd.decompress(data)))


def serialize(data):
    if data is None:
        data = {}
    content = msgpack.dumps(data)
    return bytes(zstd.compress(content))
