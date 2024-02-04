import socket
import time
import json
import os
import pickle

#PACKET TYPE
class Packet:
    def __init__(self, freq, type, curr_time, note):
        self.freq = freq
        self.type = type
        self.curr_time = curr_time
        self.note = note

#JSON READING
raw_conts = open("info.json", "r").read()
json_conts = json.loads(raw_conts)
port = int(json_conts["port"])

#SOCKET CREATION
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', port))

#LISTENING FOR CONNECTIONS
#sock.listen(5)
#conn, client_addr = sock.accept()
#print("tcp_conn from:", client_addr)
#conn.send(b'Sucessfully Connected.')

#PINGING
#while True:
#    conn.send(b'TEST')
#    time.sleep(1)

received_packets = []
packets_showing = 0

def receive_packet(packets_showing):

    #RECEVING PACKETS
    received_data = conn.recv(1024)
    received_obj = None
    if packets_showing < 4:
        #APPENDING RECEIVED PACKET
        try:
            received_obj = pickle.loads(received_data)
        except:
            pass
        if received_obj != None and received_obj.type != "":
            print(f'{received_obj.type} at {received_obj.freq}')
            print(received_obj.curr_time)
            if received_obj.note != "" and received_obj.note != " ":
                print(f'Notes: {received_obj.note}')
            print("\n")
            received_packets.append(received_obj)
            packets_showing += 1
    else:
        os.system("cls")
        packets_showing = 0
        #APPENDING RECEIVED PACKET
        try:
            received_obj = pickle.loads(received_data)
        except:
            pass
        if received_obj != None and received_obj.type != "":
            print(f'{received_obj.type} at {received_obj.freq}')
            print(received_obj.curr_time)
            if received_obj.note != "" and received_obj.note != " ":
                print(f'Notes: {received_obj.note}')
            print("\n")
            received_packets.append(received_obj)
            packets_showing += 1
    return packets_showing

while True:
    sock.listen()
    conn, client_addr = sock.accept()
    #print("tcp_conn from:", client_addr)
    conn.send(b'Sucessfully Connected.')
    choice = conn.recv(1024)
    if choice == b'SEND':
        packets_showing = receive_packet(packets_showing)
        conn.close()
    elif choice == b'REQUEST':
        serialized_packets = pickle.dumps(received_packets)
        conn.sendall(serialized_packets)
        conn.close()

    conn.close()



