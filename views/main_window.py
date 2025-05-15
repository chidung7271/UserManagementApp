# from PyQt5.QtWidgets import QMainWindow, QTabWidget
# from PyQt5.QtCore import Qt
# from controllers.pet_controller import PetController
# from controllers.schedule_controller import ScheduleController
# from controllers.health_controller import HealthController
# from controllers.finance_controller import FinanceController

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Quản lý Thú cưng")
#         self.setMinimumSize(800, 600)
        
#         # Khởi tạo các controller
#         self.pet_controller = PetController()
#         self.schedule_controller = ScheduleController()
#         self.health_controller = HealthController()
#         self.finance_controller = FinanceController()
        
#         self.init_ui()
        
#     def init_ui(self):
#         # Tạo tab widget
#         self.tabs = QTabWidget()
        
#         # Thêm các tab chức năng
#         self.tabs.addTab(self.pet_controller.view, "Hồ sơ thú cưng")
#         self.tabs.addTab(self.schedule_controller.view, "Lịch chăm sóc")
#         self.tabs.addTab(self.health_controller.view, "Theo dõi sức khỏe")
#         self.tabs.addTab(self.finance_controller.view, "Quản lý chi phí")
        
#         self.setCentralWidget(self.tabs)