import socket
import json
import time
from datetime import datetime
import pytz
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
ip_addr = json_conts["ip_addr"]

#SOCKET CREATION/CONNECTION
sock = socket.socket()
sock.connect((ip_addr, port))

conn_msg = sock.recv(1024)
print(str(conn_msg))

#PING TEST
#while True:
#    start = time.perf_counter()
#    sock.recv(1024)
#    end = time.perf_counter()
#    print("Elapsed: ", end - start)
#    time.sleep(1)
choice = input("Receive(1) Send(2) > ")
if choice == "2":
    sock.send(b'SEND')
    freq = input("Frequency(MHZ) > ")
    type = input("Type(Voice, APRS, SSTV, etc.) > ")
    tz_London = pytz.timezone('Europe/London')
    curr_time = datetime.now(tz_London)
    curr_time = curr_time.strftime("%H:%M:%S")
    note = input("Notes(Can Be Left Empty) > ")
    obj = Packet(freq, type, curr_time, note)
    serialized_obj = pickle.dumps(obj)
    sock.sendall(serialized_obj)
elif choice == "1":
    sock.send(b'REQUEST')
    received_data = sock.recv(1024)
    received_obj = pickle.loads(received_data)
    for packet in received_obj:
        print(f'{packet.type} at {packet.freq}')
        print(packet.curr_time)
        if packet.note != "" and packet.note != " ":
            print(f'Notes: {packet.note}')
        print("\n")

