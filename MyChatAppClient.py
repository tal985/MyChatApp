#!/usr/bin/env python3

import socket, sys, threading

def checkArgs():
    try:
        socket.inet_aton(ip)
    except socket.error as e:
        print(e)
        exit()

    if(port < 1 or port > 65535):
        print("ERROR: Invalid port.")
        exit()

def sendMsg():
    while True:
        client.send(bytes(input(""), "utf-8"))

if len(sys.argv) != 4:
    print("ERROR: Invalid parameters.")
    exit()

ip = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])

checkArgs()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((ip, port))
except Exception as e:
    print(e)
    exit()
client.send(name.encode())

iThread = threading.Thread(target = sendMsg)
iThread.daemon = True
iThread.start()

while True:
    try:
        data = client.recv(1024)
        if not data:
            break
        print(str(data,"utf-8"))
    except Exception as e:
        print(e)
        exit()