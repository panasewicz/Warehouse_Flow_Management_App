import snap7
from snap7.util import get_bool, get_int, get_string, get_dt, set_int

def check_connection(ip, rack, slot):
    client = snap7.client.Client()
    try:
        client.connect(ip, rack, slot)
        return client
    except Exception as e:
        print(f"No connection with PLC: {e}")
        return None

def read_plc_values(client, db_number, start_read_offset):
    try:
        db_data = client.db_read(db_number, 0, 3036)  # Reading 512 bytes from DB

        int1_offset = start_read_offset
        int2_offset = int1_offset + 2
        int3_offset = int2_offset + 2
        int4_offset = int3_offset + 2
        str_offset = int4_offset + 4
        dt_offset = str_offset + 256

        int1_value = get_int(db_data, int1_offset)
        int2_value = get_int(db_data, int2_offset)
        int3_value = get_int(db_data, int3_offset)
        int4_value = get_int(db_data, int4_offset)
        str_value = get_string(db_data, str_offset).rstrip('\x00')  # Deleting 0 byte at the end of the string
        dt_value = get_dt(db_data, dt_offset)

        return {"int1": int1_value, "int2": int2_value, "int3": int3_value, "int4": int4_value, "string": str_value, "Data_And_Time": dt_value}
    except Exception as e:
        print(f"Not able to read a value from PLC: {e}")
        return None
def write_int_value(client, db_number, write_offset, value):
    try:
        # Memory allocation for 2 bytes (int values in snap7 are stored on 2 bytes)
        data = bytearray(2)
        # Value setting
        set_int(data, 0, value)
        # Save Value in PLC
        client.db_write(db_number, write_offset, data)
        print(f"Value {value} saved in DB {db_number} with offset {write_offset}")
    except Exception as e:
        print(f"Nie udało się zapisać wartości: {e}")

def read_bool_value(client, db_number, execute_bool_offset):
    try:
        db_data = client.db_read(db_number, 0, 2992)  # Reading 1 Byte From DB

        bool_value = get_bool(db_data, execute_bool_offset, 0)

        return bool_value
    except Exception as e:
        print(f"Not able to read Bool Value From PLC: {e}")
        return None

#Bool Offset for Diffrent Readers from PLC DB.
def generate_value_offsets(num_values):
    offsets = [2]
    for i in range(1, num_values + 1):
        offsets.append(276 * i + 2)
    return offsets

#Bool Offset for Diffrent Readers from PLC DB.
def generate_scan_offsets(num_values):
    offsets = [0]
    for i in range(1, num_values):  # We start with 1, because for 0 we have already added a value to the list
        offsets.append(i * 276)  # each successive value is a multiple of 272
    return offsets

def generate_scan_offsets_write(num_values):
    offsets = [0]
    for i in range(1, num_values):  
        offsets.append(i * 272)  
    return offsets

