import socket
import time

"""
Codes:

tme   Set Timer
dir   Set Count Direction 0 down 1 up
cnt   Set Count Enable 0/1
lcl   Display Local Time (No Value)
sca   Set Score A
scb   Set Score B
spd   Set Period
sbs   Set Bonus
scr   Set Scores Enable
"""

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 60140  # The port used by the server


def send(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode("utf-8"))

while True:
    send("sbs:A")
    time.sleep(1)
    send("sbs:B")
    time.sleep(1)
