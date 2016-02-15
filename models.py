"""Simple wrapper class for DB access"""
import MySQLdb
import MySQLdb.cursors
import config

class DbConnect:
    def __init__(self, key):
        self.db = MySQLdb.connect(host = config.DB[key]['host'], user = config.DB[key]['user'], 
            passwd = config.DB[key]['passwd'], db = config.DB[key]['dbname'], cursorclass = MySQLdb.cursors.DictCursor)

    