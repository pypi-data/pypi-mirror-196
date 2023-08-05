from base import Connect
import MySQLdb

class MysqlConnect(Connect):
    
    def __init__(self, config) -> None:
        """
        config = {
            
        }
        """
        
        self.connect = MySQLdb.connect(config)