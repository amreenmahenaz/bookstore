class ScenHistVol:
    def __init__(self, db_host='localhost', db_name='volatility_db', db_user='user', db_password='password'):
        # Initialize database connection parameters
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

