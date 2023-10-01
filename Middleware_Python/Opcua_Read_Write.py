from opcua import Client, ua
from opcua.ua import VariantType

def check_connection(url):
    client = Client(url)
    try:
        client.connect()
        return client
    except Exception as e:
        print(f"No connection with OPC UA server: {e}")
        return None

def write_int_value(client, node_id, value):
    try:
        node = client.get_node(node_id)
        node_value = value
        node_value_dv = ua.DataValue(ua.Variant(node_value, ua.VariantType.Int16))
        node.set_value(node_value_dv)

        print(f"Value {node_value_dv} is saved in {node_id}")
    except Exception as e:
        print(f"Not able to save value: {e}")


def read_bool_value(client, node_id):
    try:
        node = client.get_node(node_id)
        bool_value = node.get_value()

        return bool_value
    except Exception as e:
        print(f"Not able to read Bool Value From OPC UA server: {e}")
        return None
