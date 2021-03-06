# -*- coding: utf-8 -*-
from database.dbmanager import DBManager
from help import log

__author__ = 'Nguyen Huu Giap'
from command import Command
from argument import Argument
from struct import *
import socket
import select

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
            cmd.add_byte(arg_code, byte_val)
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
    pass


def analysis_message(sock, cmd):
    """
    @param sock: client just sent message
    @param cmd: command
    @return: no return
    """
    log.log("Receive:   " + cmd.get_log())
    if cmd.code == Command.CMD_LOGIN:
        analysis_message_login(sock, cmd)
        pass
    elif cmd.code == Command.CMD_REGISTER:
        analysis_message_register(sock, cmd)
        pass
    elif cmd.code == Command.CMD_PLAYER_CHAT:
        analysis_message_chat(sock, cmd)
        pass
        """"""
    elif cmd.code == Command.CMD_LIST_FRIEND:
        analysis_message_list_friend(sock, cmd)
        pass
    elif cmd.code == Command.CMD_ADD_FRIEND:
        analysis_message_add_friend(sock, cmd)
        pass
    elif cmd.code == Command.CMD_ACCEPT_FRIEND:
        analysis_message_accept_friend(sock, cmd)
        pass
    elif cmd.code == Command.CMD_REMOVE_FRIEND:
        analysis_message_remove_friend(sock, cmd)
    else:
        pass
    return cmd


def analysis_message_login(sock, cmd):
    """
    Login Message
    @param sock:
    @param cmd:
    @return:
    """
    if db.check_user_login(cmd.get_string(Argument.ARG_PLAYER_USERNAME),
                           cmd.get_string(Argument.ARG_PLAYER_PASSWORD)):
        """Add player to list"""
        name_sock_map[cmd.get_string(Argument.ARG_PLAYER_USERNAME)] = sock
        sock_name_map[sock] = cmd.get_string(Argument.ARG_PLAYER_USERNAME)

        send_cmd = Command(Command.CMD_LOGIN)
        send_cmd.add_int(Argument.ARG_CODE, 1)
        send(sock, send_cmd)
pass


def analysis_message_register(sock, cmd):
    """
    Register message
    @param sock:
    @param cmd:
    @return:
    """
    send_cmd = Command(Command.CMD_REGISTER)
    if db.check_user_exits(cmd.get_string(Argument.ARG_PLAYER_USERNAME)):
        send_cmd.add_int(Argument.ARG_CODE, 0)
    else:
        db.add_user(cmd.get_string(Argument.ARG_PLAYER_USERNAME), cmd.get_string(Argument.ARG_PLAYER_PASSWORD))
        send_cmd.add_int(Argument.ARG_CODE, 1)
    sock.sendall(send_cmd.get_bytes())
    pass


def analysis_message_chat(sock, cmd):
    """
    Chat message
    @param sock:
    @param cmd:
    @return:
    """
    from_user = sock_name_map[sock]
    to_user = cmd.get_string(Argument.ARG_FRIEND_USERNAME, "noname")

    pass


def analysis_message_list_friend(sock, cmd):
    """
    Get list friend
    @param sock:
    @param cmd:
    @return:
    """
    sock.sendall(cmd.get_bytes())
    pass


def analysis_message_add_friend(sock, cmd):
    """
    Add friend message
    @param sock:
    @param cmd:
    @return:
    """
    send_cmd = Command(Command.CMD_ADD_FRIEND)
    if db.add_friend(cmd.get_string(Argument.ARG_PLAYER_USERNAME), cmd.get_string(Argument.ARG_FRIEND_USERNAME)):
        send_cmd.add_int(Argument.ARG_CODE, 1)
        send_cmd.add_string(Argument.ARG_MESSAGE, "Send invite friend successful!")
        #TODO send to friend invite message
    else:
        send_cmd.add_int(Argument.ARG_CODE, 0)
        send_cmd.add_string(Argument.ARG_MESSAGE, "Send invite friend failure! Please try again!")
    sock.sendall(send_cmd.get_bytes())


def analysis_message_accept_friend(sock, cmd):
    """
    Accept friend message
    @param sock:
    @param cmd:
    @return:
    """
    pass


def analysis_message_remove_friend(sock, cmd):
    """
    Remove exits friend message
    @param sock:
    @param cmd:
    @return:
    """
    pass


def check_player_online(username=""):
    if username in name_sock_map.keys():
        return True
    else:
        return False


def send(sock, send_cmd):
    sock.sendall(send_cmd.get_bytes())
    print "Send:   "+send_cmd.get_log()
    pass

HOST, PORT, RECV_BUFFER = "localhost", 9090, 4096
data = None
reading = True
"""Connection List"""
connection_list = []
"""List player loged in"""
name_sock_map = {}
sock_name_map = {}
"""Database"""
db = DBManager()
db.connect('127.0.0.1', 'root', '', 'gold_miner_online')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.setblocking(0)
server_socket.listen(5)
connection_list.append(server_socket)
print "Game server started on port " + str(PORT)
while True:
    # Get the list sockets which are ready to be read through select
    read_sockets, write_sockets, error_sockets = select.select(connection_list, [], [])
    for sock in read_sockets:
        #New connection
        if sock == server_socket:
            # Handle the case in which there is a new connection received through server_socket
            sockfd, addr = server_socket.accept()
            connection_list.append(sockfd)
            log.log("Have connection from :" + str(addr))
        #Some incoming message from a client
        else:
            # Data received from client, process it
            try:
                #In Windows, sometimes when a TCP program closes abruptly,
                # a "Connection reset by peer" exception will be thrown
                data = sock.recv(RECV_BUFFER)
                if data:
                    read(sock, data)
            except IOError as err:
                print 'My exception occurred, value:', err.message
                print "Client (%s, %s) is offline" % addr
                sock.close()
                connection_list.remove(sock)
                continue
server_socket.close()
