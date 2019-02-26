#!/usr/bin/env python3

import socket, sys, threading

def checkArgs():
    try:
        socket.inet_aton(ip)
    except socket.error:
        print("ERROR: Invalid IP.")
        exit()

    if(port < 1 or port > 65535):
        print("ERROR: Invalid port.")
        exit()

def dataHandler(connection, address):
    name = str(connection.recv(1024), "utf-8")
    shortCString = "[" + name + "] has connected."
    longCString = str(address[0]) + ":" + str(address[1]) + " " + shortCString
    print (longCString)

    for c in clientList:
        c.send(bytes(shortCString, "utf-8"))

    while True:
        data = connection.recv(1024)
        if data:
            msg = str("[" + name + "]: " + str(data, "utf-8"))
            print (msg)
            for c in clientList:
                c.send(bytes(msg, "utf-8"))
        else:
            shortDString = "[" + name + "] has disconnected."
            longDString = str(address[0]) + ":" + str(address[1]) + " " + shortDString
            print (longDString)
            for c in clientList:
                c.send(bytes(shortDString, "utf-8"))
            clientList.remove(connection)
            connection.close()
            break
        
if len(sys.argv) != 3:
    print("ERROR: Invalid parameters.")
    exit()

clientList = []
ip = str(sys.argv[1])
port = int(sys.argv[2])

checkArgs()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((ip, port))
except:
    print("ERROR: Connection refused.")
    exit()
server.listen(1)

print("STATUS: Waiting for incoming connections.")
while True:
    connection = None
    try:
        connection, address = server.accept()
        clientList.append(connection)
        iThread = threading.Thread(target = dataHandler, args = (connection, address))
        iThread.daemon = True
        iThread.start()
    except:
        if connection is not None:
            clientList.remove(connection)
        print ("nani?!?")
        exit()