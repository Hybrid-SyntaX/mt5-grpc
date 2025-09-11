from google.protobuf.timestamp_pb2 import Timestamp

def timestamp_to_proto(value):
    ts = Timestamp()
    ts.FromMicroseconds(value)
    return ts
