import threading
from SQL_Communication import insert_to_database, fetch_data_from_database
from Put_Get import check_connection, read_bool_value, read_plc_values, \
    generate_value_offsets, generate_scan_offsets
from Opcua_Read_Write import write_int_value
from Opcua_Read_Write import read_bool_value as rd_opcua
from Opcua_Read_Write import check_connection as check_connection_opc

plc_lock = threading.Lock()
def thread_function_read(client, db_number_read, offset_value, offset_scan):
    with plc_lock:
        try:
            bool_value_read = read_bool_value(client, db_number_read, offset_scan)
            if bool_value_read:
                values = read_plc_values(client, db_number_read, offset_value)
                if values:
                    insert_to_database(values)
        except Exception as e:
            print(f"Communication with PLC Lost. Error: {e}")

def thread_function_write(client, node_id_send, node_id_data, value):
    with plc_lock:  # Acquire the lock before accessing the PLC
        try:
            bool_value_write = rd_opcua(client, node_id_send)
            if bool_value_write:
                write_int_value(client, node_id_data, value)
        except Exception as e:
            print(f"Communication with PLC Lost. Error: {e}")

def thread_fetch_data(client, node_id_send):
    with plc_lock:
        try:
            bool_value_write = rd_opcua(client, node_id_send)
            if bool_value_write:
                data = fetch_data_from_database()
                data_list = []
                for i, row in enumerate(data, start=0):
                    data_list.append([row[0], row[1], row[2]])
                    write_int_value(client, f'ns=3;s="Station_Buffer"."Write_Buffer"[{i}]."Order_Station_ID"', row[0])
                    write_int_value(client, f'ns=3;s="Station_Buffer"."Write_Buffer"[{i}]."Barcode"', row[1])
                    write_int_value(client, f'ns=3;s="Station_Buffer"."Write_Buffer"[{i}]."Order"', row[2])

        except Exception as e:
            print(f"Communication with PLC or database failed. Error: {e}")

def main():
    ip = "192.168.0.1"
    rack = 0
    slot = 1
    db_number_read = 800
    url = "opc.tcp://192.168.0.1:4840"
    node_id_send_2 = 'ns=3;s="Scanners_db_Write"."Scanner_Write"[2]."Send_Data"'
    value = []
    offsets_value = generate_value_offsets(3)
    offsets_scan = generate_scan_offsets(3)
    client = check_connection(ip, rack, slot)
    client_opc = check_connection_opc(url)
    if client and client_opc:
        while True:
            thread_read = threading.Thread(target=thread_function_read,
                                           args=(client, db_number_read, offsets_value[1], offsets_scan[1]))
            thread_fetch = threading.Thread(target=thread_fetch_data,
                                            args=(client_opc, node_id_send_2))

            thread_read.start()
            thread_fetch.start()

            # wait for both threads to complete
            thread_read.join()
            thread_fetch.join()
    else:
        print("No possibility to connect with PLC.")

if __name__ == "__main__":
    main()
