
__author__ = 'Nguyen Huu Giap'
import SocketServer
from DBManager import DBManager
from command import Command
from argument import Argument
"""
@author: giapnh
"""


class MyServer(SocketServer.StreamRequestHandler):
    HOST, PORT = "localhost", 9999
    data = None
    reading = True
    db = DBManager()
    db.connect('127.0.0.1', 'root', '', 'oot_online')

    def handle(self):
        try:
            if self.reading:
                self.data = self.rfile.readline().strip()
                self.analysis_message(self.data)
        except IOError:
            pass

    def analysis_message(self, data):
        cmd = Command.read(data)
        #Receive message
        print "Receive:   " + cmd.to_string()
        if cmd.code == Command.CMD_LOGIN:
            if self.db.check_user_exits(cmd.get_string(Argument.ARG_LOGIN_USERNAME)):
                send_cmd = Command(Command.CMD_LOGIN)
                send_cmd.add_int(Argument.ARG_CODE, 1)
                self.send(send_cmd)
                pass
        elif cmd.code == Command.CMD_REGISTER:
            print "cmd register"
        else:
            print "default"
        return data

    def send(self, send_cmd):
        self.wfile.write(send_cmd.to_string())
        print "Send  :" + send_cmd.to_string()
        pass

if __name__ == "__main__":
    #Start server
    server = SocketServer.TCPServer((MyServer.HOST, MyServer.PORT), MyServer)
    server.serve_forever()


