# -*- coding: utf-8 -*-
__author__ = 'Nguyen Huu Giap'
import MySQLdb


class DBManager:
    #Static instance
    db = None

    def __init__(self):
        pass

    def connect(self, host, user, password, db_name):
        try:
            self.db = MySQLdb.connect(host, user, password, db_name)
            print "Init database manager successful"
        except MySQLdb.Error,e:
             print "Error %d: %s" % (e.args[0], e.args[1])

    """
    Check if user exits
    """
    def check_user_exits(self, username= ""):
        c = self.db.cursor()
        c.execute("""SELECT * FROM user where u_username = %s""", (username,))
        if c.rowcount == 1:
            print "Exits: " + username
            return True
        else:
            return False

    """
    Close connection to mysql
    """
    def close(self):
        self.db.close()


