import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from model.user_model import User
from database.db_connector import DatabaseConnector

class LoginController:
    def __init__(self, ui_file):
        self.window = uic.loadUi(ui_file)
        self.window.tabWidget.tabBar().setVisible(False)
        self.db_connector = DatabaseConnector()
        self.setup_events()

    def setup_events(self):
        self.window.pushButton_2.clicked.connect(self.login)
        self.window.pushButton_3.clicked.connect(self.register)
        self.window.action_ng_k.triggered.connect(self.switch_to_register)
        self.window.action_ng_nh_p.triggered.connect(self.switch_to_login)

    def switch_to_register(self):
        self.window.tabWidget.setCurrentIndex(1)
        self.clearfieldsregister()
    
    def switch_to_login(self):
        self.window.tabWidget.setCurrentIndex(0)
        self.clearfieldslogin()

    def clearfieldslogin(self):
        self.window.lineEdit_3.clear()
        self.window.lineEdit_4.clear()
        
    def clearfieldsregister(self):
        self.window.lineEdit_5.clear()
        self.window.lineEdit_6.clear()
        self.window.lineEdit_7.clear()
        
    def login(self):
        username = self.window.lineEdit_3.text()
        password = self.window.lineEdit_4.text()

        if not username or not password:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập đầy đủ thông tin đăng nhập.")
            return

        user = User(self.db_connector, username, password)
        if user.login():
            QMessageBox.information(self.window, "Thành công", "Đăng nhập thành công!")
            from controller.pet_controller import PetController
            self.pet_controller = PetController("views/MainWindow.ui", user.get_user_id(),self.db_connector)
            self.pet_controller.window.show()
            self.window.close()
        else:
            QMessageBox.warning(self.window, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def register(self):
        username = self.window.lineEdit_5.text()
        password = self.window.lineEdit_6.text()
        confirm_password = self.window.lineEdit_7.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập đầy đủ thông tin đăng ký.")
            return

        if password != confirm_password:
            QMessageBox.warning(self.window, "Lỗi", "Mật khẩu không khớp.")
            return

        user = User(self.db_connector, username, password)
        if user.register():
            QMessageBox.information(self.window, "Thành công", "Đăng ký thành công!")
        else:
            QMessageBox.warning(self.window, "Lỗi", "Đăng ký không thành công. Tên đăng nhập có thể đã tồn tại.")

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     login_controller = LoginController("views/Login.ui")
#     login_controller.window.show()
#     sys.exit(app.exec_())