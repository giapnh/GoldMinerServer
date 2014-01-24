__author__ = 'Nguyen Huu Giap'
import socket
from command import Command
from argument import Argument

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))
while True:
    data = client.recv(1000)
    print len(bytearray(data))
    cmd = Command(Command.CMD_PLAYER_CHAT)
    cmd.add_string(Argument.ARG_MESSAGE, "chat")
    client.send(cmd.get_bytes())
