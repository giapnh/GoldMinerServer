__author__ = 'Nguyen Huu Giap'


class Argument:
    #region Fields and Constants
    LONG = 8
    INT = 4
    SHORT = 2
    BYTE = 1
    STRING = 10
    RAW = 11

    type = INT
    number_value = 0
    string_value = ""
    byte_value = bytes()

    def __init__(self):
        pass

    def __init__(self, _type):
        """

        @param _type: Data type
        """
        self.type = _type

    def __init__(self, _type, long_val):
        """
        @param _type: Data type
        @param long_val: Long type value
        """
        self.type = _type
        self.number_value = long_val

    def __init__(self, _type, str_val):
        """

        @param _type:
        @param str_val:
        @return:
        """
        self.type = _type
        self.string_value = str_val

    def get_log(self):
            s = ""
            if self.type == self.SHORT:
                s += "short: " + self.number_value
            elif type == self.INT:
                s += "int: " + self.number_value
            elif type == self.STRING:
                s += "String: " + self.string_value
            elif type == self.RAW:
                s += "Raw: " + len(self.byte_value)
            elif type == self.BYTE:
                s += "Byte: " + self.number_value
            elif type == self.LONG:
                s += "Long: " + self.number_value
            return s

    def to_string(self):
        if None != self.string_value:
            return self.string_value
        if None != self.byte_value:
            s = ""
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





