from ctypes import c_ushort

__author__ = 'Nguyen Huu Giap'
import argument


class Command:
    code = 0
    #Command code
    CMD_INVALID = -1
    CMD_REGISTER = 1
    CMD_LOGIN = 2

    def __init__(self, code):
        self.args = {}
        self.code = code

    #read from data
    @staticmethod
    def read(data=""):
        items = data.split('|')
        cmd = Command(int(items[0]))
        #number of items
        num_arg = int(items[1])
        # if num_arg > (len(items) - 2)/3:
        #     pass
        for i in range(0, num_arg):
            code = int(items[3 * i + 2])
            type = int(items[3 * i + 3])
            val = items[3 * i + 4]
            if type == argument.Argument.STRING:
                cmd.add_argument(code, argument.Argument(code, val))
        return cmd

    #Add argument
    def add_argument(self, arg_code, arg):
        self.args[arg_code] = arg
        return self

    def add_short(self, arg_code, long_val):
        self.add_argument(arg_code, argument.Argument(argument.Argument.SHORT, long_val))
        return self

    def add_int(self, arg_code, long_val):
        self.add_argument(arg_code, argument.Argument(argument.Argument.INT, long_val))
        return self

    def add_long(self, arg_code, long_val):
        self.add_argument(arg_code, argument.Argument(argument.Argument.LONG, long_val))
        return self

    def add_string(self, arg_code, str_val):
        self.add_argument(arg_code, argument.Argument(argument.Argument.STRING, str_val))
        return self

    def get_string(self, code, default= ""):
        arg = self.args[code]
        if None != arg:
            return arg.to_string()
        return default

    def get_int(self, code, default= 0):
        arg = self.args[code]
        if None != arg:
            return int(arg.number_value)
        return int(default)

    def get_short(self, code, default= 0):
        arg = self.args[code]
        if None != arg:
            return c_ushort(arg.number_value)
        return c_ushort(default)

    def get_long(self, code, default= 0):
        arg = self.args[code]
        if None != arg:
            return arg.number_value
        return long(default)

    def get_boolean(self, code, default= "False"):
        arg = self.args[code]
        if None != arg:
            return arg.number_value != 0
        return default

    def to_string(self):
        res = ""
        #1. command code
        res += str(self.code)
        #2. number of argument
        res += "|"
        res += str(len(self.args))

        keys = self.args.keys()
        for key in keys:
            #3. argument
            res += "|" + str(key)
            arg = self.args[key]
            res += "|" + str(arg.type)
            res += "|" + str(arg.to_string())
        return res

    @staticmethod
    def get_command_name(code):
        return "CmdName"

    def get_log(self):
        s = "************Command: " + self.get_command_name(self.code) + "[" + self.code + "]\n"
        keys = self.args
        for key in keys:
            arg = self.args[key]
            s += "    " + argument.Argument.get_argument_as_string(key) + "[" + key + "]" + arg.to_string() + "\n"
        s += "\n"
        return s

