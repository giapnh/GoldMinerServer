__author__ = 'Nguyen Huu Giap'
from struct import *

class Argument:
    #region Fields and Constants
    LONG = 8
    INT = 4
    SHORT = 2
    BYTE = 1
    STRING = 10
    RAW = 11

    type = 0
    number_value = 0
    string_value = ""
    byte_value = bytes()

    def __init__(self, _type, value):
        """

        @param _type: Data type
        """
        if _type is not None:
            self.type = _type
            if value is not None:
                if self.type == self.BYTE or self.type == self.SHORT or self.type == self.INT or self.type == self.LONG:
                    self.number_value = value
                elif self.type == self.STRING:
                    self.string_value = value
                else:
                    self.byte_value = value
        pass

    def get_log(self):
            s = ""
            if self.type == self.SHORT:
                s += "short: " + self.number_value
            elif self.type == self.INT:
                s += "int: " + self.number_value
            elif self.type == self.STRING:
                s += "String: " + self.string_value
            elif self.type == self.RAW:
                s += "Raw: " + len(self.byte_value)
            elif self.type == self.BYTE:
                s += "Byte: " + self.number_value
            elif self.type == self.LONG:
                s += "Long: " + self.number_value
            return s


    def to_string(self):
        if self.type == self.STRING:
            return self.string_value
        if self.type == self.RAW:
            try:
                s = self.byte_value.decode('utf-8')
                return s
            except Exception:
                return "ex"
        else:
            return self.number_value


    @staticmethod
    def get_argument_as_string(code):
        return "ArgName"

    ARG_CODE = 0
    ARG_LOGIN_USERNAME = 20
    ARG_LOGIN_PASSWORD = 21





