# -*- coding: utf-8 -*-
__author__ = 'Nguyen Huu Giap'
import SocketServer
from DBManager import DBManager
from command import Command
from argument import Argument
from struct import *
"""
@author: giapnh
"""




    def handle(self):
        try:
            if self.reading:
                #Read command length
                self.data = bytearray(self.request.recv(1024))
                self.read()
        except IOError:
            pass

    def read(self):
        """
        Create command from received data

        """
        read_count = 0
        code = int(unpack("<H", self.data[0:2])[0])
        read_count += 2
        cmd = Command(code)
        num_arg = int(unpack("<H", self.data[2:4])[0])
        read_count += 2
        for i in range(0, num_arg, 1):
            #Read all argument
            arg_code = int(unpack("<H", self.data[read_count:read_count+2])[0])
            read_count += 2
            #Argument type
            arg_type = int(unpack("B", self.data[read_count:read_count + 1])[0])
            read_count += 1
            if arg_type == Argument.STRING:
                #string len
                str_len = int(unpack("<I", self.data[read_count:read_count + 4])[0])
                read_count += 4
                str_val = str(unpack(str(str_len)+"s", self.data[read_count:read_count + str_len])[0])
                read_count += str_len
                cmd.add_string(arg_code, str_val)
            elif arg_type == Argument.RAW:
                raw_len = int(unpack("<I", self.data[read_count:read_count + 4])[0])
                read_count += 4
                raw_data = self.data[read_count, read_count + raw_len]
                read_count += raw_len
                cmd.add_raw(arg_code, raw_data)
            elif arg_type == Argument.BYTE:
                byte_val = int(unpack("B", self.data[read_count:read_count + 1])[0])
                read_count += 1
                self.add_byte(arg_code, byte_val)
            elif arg_type == Argument.SHORT:
                short_val = int(unpack("<H", self.data[read_count:read_count + 2])[0])
                read_count += 2
                cmd.add_short(arg_code, short_val)
            elif arg_type == Argument.INT:
                int_val = int(unpack("<I", self.data[read_count:read_count + 4])[0])
                read_count += 4
                cmd.add_int(arg_code, int_val)
            elif arg_type == Argument.LONG:
                long_val = long(unpack("<L", self.data[read_count:read_count + 8])[0])
                read_count += 8
                cmd.add_long(arg_code, long_val)
        self.analysis_message(cmd)
        pass

    def analysis_message(self, cmd):
        #Receive message
        print "Receive:   " + cmd.get_log()
        if cmd.code == Command.CMD_LOGIN:
            if self.db.check_user_exits(cmd.get_string(Argument.ARG_LOGIN_USERNAME)):
                send_cmd = Command(Command.CMD_LOGIN)
                send_cmd.add_int(Argument.ARG_CODE, 1)
                self.send(send_cmd)
                pass
        elif cmd.code == Command.CMD_REGISTER:
            pass
        else:
            pass
        return cmd

    def send(self, send_cmd):
        self.request.sendall(send_cmd.get_bytes())
        print "Send:   "+send_cmd.get_log()
        pass


HOST, PORT = "localhost", 9999
data = None
reading = True
db = DBManager()
db.connect('127.0.0.1', 'root', '', 'oot_online')



