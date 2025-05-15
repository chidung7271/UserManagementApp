import bcrypt

class User:
    def __init__(self, db, username, password, user_id = None):
        self.db = db
        self.id = user_id
        self.username = username
        self.password = password

    def register(self):
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        values = (self.username, hashed_password.decode('utf-8'))
        try:
            self.db.execute_query(query, values)
            return True
        except Exception as e:
            print(f"Error during registration: {e}")
            return False

    def login(self):
        query = "SELECT * FROM users WHERE username = %s"
        values = (self.username,)
        result = self.db.fetch_one(query, values)
        if result:
            stored_password = result[2]  # Assuming password is the third column
            if bcrypt.checkpw(self.password.encode('utf-8'), stored_password.encode('utf-8')):
                return True
            else:
                return False
        else:
            return False

    def get_user_id(self):
        
        query = "SELECT user_id FROM users WHERE username = %s"
        values = (self.username,)
        result = self.db.fetch_one(query, values)
        if result:
            self.id = result[0]
            return result[0]
        return None