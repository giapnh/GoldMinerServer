from ctypes import c_ushort
from argument import Argument
from struct import *
__author__ = 'Nguyen Huu Giap'
"""
<@author Steve Giap
"""


class Command:
    code = 0
    #Command code
    CMD_INVALID = -1
    CMD_REGISTER = 1
    CMD_LOGIN = 2
    CMD_PLAYER_INFO = 3
    CMD_PLAYER_CHAT = 10

    def __init__(self, code):
        self.args = {}
        self.code = code

    #Add argument
    def add_argument(self, arg_code, arg):
        self.args[arg_code] = arg
        return self

    def add_byte(self, arg_code=0, long_val=int()):
        self.add_argument(arg_code, Argument(Argument.BYTE, long_val))
        return self

    def add_short(self, arg_code=0, long_val=c_ushort()):
        self.add_argument(arg_code, Argument(Argument.SHORT, long_val))
        return self

    def add_int(self, arg_code=0, long_val=int()):
        self.add_argument(arg_code, Argument(Argument.INT, long_val))
        return self

    def add_long(self, arg_code=0, long_val=long()):
        self.add_argument(arg_code, Argument(Argument.LONG, long_val))
        return self

    def add_string(self, arg_code=0, str_val=str()):
        self.add_argument(arg_code, Argument(Argument.STRING, str_val))
        return self

    def add_raw(self, arg_code=0, raw_val=bytes()):
        self.add_argument(arg_code, Argument(Argument.RAW, raw_val))
        return self

    def get_string(self, code=0, default=""):
        arg = self.args[code]
        if None != arg:
            return arg.to_string()
        return default

    def get_int(self, code, default=0):
        arg = self.args[code]
        if None != arg:
            return int(arg.number_value)
        return int(default)

    def get_short(self, code, default=0):
        arg = self.args[code]
        if None != arg:
            return c_ushort(arg.number_value)
        return c_ushort(default)

    def get_long(self, code, default=0):
        arg = self.args[code]
        if None != arg:
            return arg.number_value
        return long(default)

    def get_boolean(self, code, default=False):
        arg = self.args[code]
        if None != arg:
            return arg.number_value != 0
        return default

    # def to_string(self):
    #     res = ""
    #     #1. command code
    #     res += str(self.code)
    #     #2. number of argument
    #     res += "|"
    #     res += str(len(self.args))
    #
    #     keys = self.args.keys()
    #     for key in keys:
    #         #3. argument
    #         res += "|" + str(key)
    #         arg = self.args[key]
    #         res += "|" + str(arg.type)
    #         res += "|" + str(arg.to_string())
    #     return res

    @staticmethod
    def get_command_name(code):
        return "CmdName"

    def get_log(self):
        s = "************Command: " + self.get_command_name(self.code) + "[" + str(self.code) + "]\n"
        keys = self.args.keys()
        for key in keys:
            arg = self.args[key]
            s += "    " + Argument.get_argument_as_string(key) + "[" + str(key) + "]" + str(arg.to_string()) + "\n"
        s += "\n"
        return s

    def get_bytes(self):
        #Size
        cmd_len = 0
        #command code
        cmd_len += 2
        #number of argument
        cmd_len += 2
        keys = self.args.keys()
        for key in keys:
            arg = self.args[key]
            #argument code
            cmd_len += 2
            #argument data type
            cmd_len += 1
            arg_type = arg.type
            if arg_type == Argument.STRING:
                #string data length
                cmd_len += 4
                cmd_len += len(str(arg.string_value).encode())
            elif arg_type == Argument.RAW:
                cmd_len += 4
                cmd_len += len(arg.byte_value)
            else:
                cmd_len += int(arg_type)
        #Buffer
        buff = bytearray(cmd_len)
        offset = 0
        pack_into("<H", buff, 0, self.code)
        offset += 2
        pack_into("<H", buff, offset, len(self.args))
        offset += 2
        keys = self.args.keys()
        for key in keys:
            arg = self.args[key]
            pack_into("<H", buff, offset, key)
            offset += 2
            pack_into("<B", buff, offset, arg.type)
            offset += 1
            if arg.type == Argument.BYTE:
                pack_into("<B", buff, offset, arg.number_value)
                offset += 1
            elif arg.type == Argument.SHORT:
                pack_into("<H", buff, offset, arg.number_value)
                offset += 2
            elif arg.type == Argument.INT:
                pack_into("<I", buff, offset, arg.number_value)
                offset += 4
            elif arg.type == Argument.LONG:
                pack_into("<L", buff, offset, arg.number_value)
                offset += 8
            elif arg.type == Argument.STRING:
                str_len = len(str(arg.string_value).encode())
                pack_into("<I", buff, offset, str_len)
                offset += 4
                pack_into(str(str_len)+"s", buff, offset, str(arg.string_value))
                offset += str_len
            else:
                raw_len = len(arg.byte_value)
                buff[offset:offset+raw_len] = arg.byte_value
        return buff