import mysql.connector
from mysql.connector import Error

class DatabaseConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            print("Đang kết nối đến cơ sở dữ liệu...")
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="pet_management"
            )
            if self.connection.is_connected():
                print("Kết nối database thành công!")
                self.cursor = self.connection.cursor()
            else:
                print("Kết nối database thất bại!")
        except Error as e:
            print(f"Lỗi kết nối database: {e}")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            print(f"Lỗi thực thi query: {e}")
            return False

    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Lỗi lấy dữ liệu: {e}")
            return None

    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error as e:
            print(f"Lỗi lấy dữ liệu: {e}")
            return None

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Đã đóng kết nối database")