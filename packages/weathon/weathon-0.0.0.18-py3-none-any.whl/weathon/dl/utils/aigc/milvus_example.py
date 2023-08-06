
from milvus import default_server
from pymilvus import connections, utility
with default_server:
    print("connecting ..")
    connections.connect("127.0.0.1", port=9092)

    print(f"current milvus server version:{utility.get_server_version()}" )