#!/usr/bin/env python3
import xmpp
from struct import pack, unpack 
import socket, datetime
from time import sleep
from yaml import safe_load

def main():
    with open("config.yaml", "r") as file:
        config = safe_load(file)
    mumble_server = config["mumble_server"]
    mumble_port = config["mumble_port"]
    oldusers, maxusers = get_users(mumble_server, mumble_port)
    print("started server")
    while 1:
        users, maxusers = get_users(mumble_server, mumble_port)
        if users > oldusers: # notify only if increase
            send_message(config["subscribers"], f"Mumble {mumble_server}: {users}/{maxusers} users", config["xmpp_jid"], config["xmpp_password"])
        oldusers = users
        sleep(config["polling_rate"])

def send_message(receivers, message, jabberid, password):
    "Send xmpp message to receiver"
    jid = xmpp.protocol.JID(jabberid)
    connection = xmpp.Client(server=jid.getDomain(), debug=[])
    connection.connect()
    connection.auth(user=jid.getNode(), password=password, resource=jid.getResource())
    for receiver in receivers:
        connection.send(xmpp.protocol.Message(to=receiver, body=message))

# Adapted from https://raw.githubusercontent.com/mumble-voip/mumble-scripts/master/Non-RPC/mumble-ping.py
def get_users(address: str, port: int) -> tuple:
    "Gets the number of users and max users on server)"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    buf = pack(">iQ", 0, datetime.datetime.now().microsecond)
    s.sendto(buf, (address, port))
    try:
        data, addr = s.recvfrom(1024)
    except socket.timeout:
        print(f"{time.time()}:NaN:NaN")
        return (0,0)
    r = unpack(">bbbbQiii", data)
    users = r[5]
    max_users = r[6]
    return (users, max_users)
if __name__ == '__main__':
    main()
