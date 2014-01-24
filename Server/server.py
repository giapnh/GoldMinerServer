# -*- coding: utf-8 -*-
__author__ = 'Nguyen Huu Giap'
import SocketServer
from DBManager import DBManager
from command import Command
from argument import Argument
from struct import *
import socket
import select
import log
"""
@author: giapnh
"""


def read(sock, data):
    """
    Analysis command
    @param sock the socket of client
    @param data the read data
    """
    read_count = 0
    code = int(unpack("<H", data[0:2])[0])
    read_count += 2
    cmd = Command(code)
    num_arg = int(unpack("<H", data[2:4])[0])
    read_count += 2
    for i in range(0, num_arg, 1):
        """Read all argument"""
        arg_code = int(unpack("<H", data[read_count:read_count+2])[0])
        read_count += 2
        #Argument type
        arg_type = int(unpack("B", data[read_count:read_count + 1])[0])
        read_count += 1
        if arg_type == Argument.STRING:
            #string len
            str_len = int(unpack("<I", data[read_count:read_count + 4])[0])
            read_count += 4
            str_val = str(unpack(str(str_len)+"s", data[read_count:read_count + str_len])[0])
            read_count += str_len
            cmd.add_string(arg_code, str_val)
        elif arg_type == Argument.RAW:
            raw_len = int(unpack("<I", data[read_count:read_count + 4])[0])
            read_count += 4
            raw_data = data[read_count, read_count + raw_len]
            read_count += raw_len
            cmd.add_raw(arg_code, raw_data)
        elif arg_type == Argument.BYTE:
            byte_val = int(unpack("B", data[read_count:read_count + 1])[0])
            read_count += 1
            add_byte(arg_code, byte_val)
        elif arg_type == Argument.SHORT:
            short_val = int(unpack("<H", data[read_count:read_count + 2])[0])
            read_count += 2
            cmd.add_short(arg_code, short_val)
        elif arg_type == Argument.INT:
            int_val = int(unpack("<I", data[read_count:read_count + 4])[0])
            read_count += 4
            cmd.add_int(arg_code, int_val)
        elif arg_type == Argument.LONG:
            long_val = long(unpack("<L", data[read_count:read_count + 8])[0])
            read_count += 8
            cmd.add_long(arg_code, long_val)
    analysis_message(sock, cmd)
    print "2"
    pass

def analysis_message(sock, cmd):
    #Receive message
    print "Receive:   " + cmd.get_log()
    if cmd.code == Command.CMD_LOGIN:
        if db.check_user_exits(cmd.get_string(Argument.ARG_LOGIN_USERNAME)):
            send_cmd = Command(Command.CMD_LOGIN)
            send_cmd.add_int(Argument.ARG_CODE, 1)
            send(sock, send_cmd)
            pass
    elif cmd.code == Command.CMD_REGISTER:
        pass
    elif cmd.code == Command.CMD_PLAYER_CHAT:
        pass
    elif cmd.code == Command.CMD_ADD_FRIEND:
        log.log("Add friend...")
        pass
    else:
        pass
    return cmd

def send(sock, send_cmd):
    request.sendall(send_cmd.get_bytes())
    print "Send:   "+send_cmd.get_log()
    pass

HOST, PORT, RECV_BUFFER = "localhost", 9999, 4096
data = None
reading = True
"""Connection List"""
connection_list = []
"""Database"""
db = DBManager()
db.connect('127.0.0.1', 'root', '', 'oot_online')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST,PORT))
server_socket.setblocking(0)
server_socket.listen(5)
connection_list.append(server_socket)
print "Game server started on port " + str(PORT)
while True:
    # Get the list sockets which are ready to be read through select
    read_sockets,write_sockets,error_sockets = select.select(connection_list,[],[])
    for sock in read_sockets:
        #New connection
        if sock == server_socket:
            # Handle the case in which there is a new connection recieved through server_socket
            sockfd, addr = server_socket.accept()
            connection_list.append(sockfd)
            log.log("Have connection from :" + str(addr))
        #Some incoming message from a client
        else:
            # Data recieved from client, process it
            try:
                #In Windows, sometimes when a TCP program closes abruptly,
                # a "Connection reset by peer" exception will be thrown
                data = sock.recv(RECV_BUFFER)
                if data:
                    read(sock, data)
            except IOError as err:
                print 'My exception occurred, value:', e.value
                print "Client (%s, %s) is offline" % addr
                sock.close()
                connection_list.remove(sock)
                continue
server_socket.close()
