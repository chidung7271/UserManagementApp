# -*- coding: utf-8 -*-
from database.db_connector import DatabaseConnector
import mysql.connector
from PyQt5.QtWidgets import QApplication
import sys
from controller.login_controller import LoginController
if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_controller = LoginController("views/Login.ui")
    login_controller.window.show()
    
    sys.exit(app.exec_())
    
    