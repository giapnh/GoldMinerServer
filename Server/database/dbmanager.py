# -*- coding: utf-8 -*-
__author__ = 'Nguyen Huu Giap'
import MySQLdb
import hashlib

class DBManager:
    #Static instance
    db = None

    def __init__(self):
        pass

    def connect(self, host, user, password, db_name):
        try:
            self.db = MySQLdb.connect(host, user, password, db_name)
            print "Init database manager successful"
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
    """
    Check user exits?
    """
    def check_user_exits(self, username=""):
        c = self.db.cursor()
        c.execute("""SELECT * FROM user where u_username = %s""",
                  (username, ))
        if c.rowcount == 1:
            print "Check user: " + username + ": Exits!!!"
            return True
        else:
            print "Check user: " + username + ": Not Exits!!!"
            return False
    """
    Check if account is valid
    """
    def check_user_login(self, username="", password=""):
        c = self.db.cursor()
        c.execute("""SELECT * FROM user where u_username = %s and u_password = %s""",
                  (username, hashlib.md5(password).hexdigest(), ))
        if c.rowcount == 1:
            print "Check user: " + username + ": Exits!!!"
            return True
        else:
            print "Check user: " + username + ":Not Exits!!!"
            return False
    """
    Add user to database when has user register
    """
    def add_user(self, username="", password="", os=0):
        c = self.db.cursor()
        c.execute("""INSERT INTO user(u_username, u_password) VALUES(%s, %s)""",
                  (username, password, str(os), ))
        self.db.commit()
        pass
    """
    Get player information: username, level, ...
    """
    def get_user_info(self, username=""):
        c = self.db.cursor()
        c.execute("""SELECT u_username,u_level,u_level_up_point
         ,u_cup FROM user where u_username = %s""", (username, ))
        if c.rowcount == 1:
            row = c.fetchone()
            info = {"u_username": row[0], "u_level": row[1], "u_level_up_point": row[2], "u_cup": row[3]}
            return info
        else:
            return None
    """
    Close connection to mysql
    """
    def close(self):
        self.db.close()


