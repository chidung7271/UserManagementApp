import datetime
import sys
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QTableWidgetItem, 
                            QHeaderView, QApplication, QFileDialog, QLabel,QVBoxLayout)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap,QTextCharFormat, QBrush, QColor, QFont
from PyQt5 import uic
from config.draw import PlotCanvas
from database.db_connector import DatabaseConnector
from model.pet_model import Pet
from model.calendar_model import Calendar
from model.physical_model import Physical
class PetController:
    def __init__(self, ui_file, user_id, db):
        self.user_id = user_id
        self.db_connector = db
        self.window = uic.loadUi(ui_file)
        self.view = self.window
        self.pets = []
        self.calendar_events = []
        self.physicals = []
        self.current_image_path = None
        self.is_chart_active = True
        self.setup_ui()
        self.setup_events()
        
        
        
    def setup_ui(self):
        self.window.tabWidget.tabBar().setVisible(False)
        self.window.setWindowTitle("Quản lý thú cưng")
        self.window.setFixedSize(self.window.size())
        self.window.petTable.setColumnCount(9)
        self.window.petTable.setHorizontalHeaderLabels([
            "ID", "Tên", "Giống", "Tuổi", "Giới tính",
            "Ngày nhận nuôi", "Tình trạng sức khỏe", "Ghi chú","Hình ảnh"
        ])
        header = self.window.petTable.horizontalHeader()
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.window.petTable_2.setColumnCount(6)
        self.window.petTable_2.setHorizontalHeaderLabels([
        "ID","Tên thú cưng", "Cân nặng", "Chiều cao", "Ngày kiểm tra", "Ghi chú",
        ])
        header2 = self.window.petTable_2.horizontalHeader()
        header2.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(QHeaderView.Stretch)
        self.load_pets()
        self.load_calendar()
        self.load_physical()
        self.populate_pet_combobox()
        self.populate_physical_combobox()
        self.populate_chart_combobox()
    def populate_physical_combobox(self):
        self.window.comboBox_3.clear()
        for pet in self.pets:
            self.window.comboBox_3.addItem(pet.name, pet.id)
    
    def populate_chart_combobox(self):
        self.window.comboBox_6.clear()
        for pet in self.pets:
            self.window.comboBox_6.addItem(pet.name, pet.id)
    
    def populate_pet_combobox(self):
        self.window.comboBox_4.clear()
        for pet in self.pets:
            self.window.comboBox_4.addItem(pet.name, pet.id)
    def setup_events(self):
        self.window.pushButton.clicked.connect(self.switch_to_add_tab)
        self.window.pushButton_2.clicked.connect(self.refresh_pet)
        self.window.pushButton_3.clicked.connect(self.delete_pet)
        self.window.pushButton_5.clicked.connect(self.switch_to_update_tab)
        self.window.btnSelectImage.clicked.connect(self.select_image)
        self.window.btnAddPet.clicked.connect(self.add_pet)
        self.window.btnUpdatePet.clicked.connect(self.update_pet)
        self.window.btnDatLich.clicked.connect(self.add_calendar_event)
        self.window.calendarWidget.selectionChanged.connect(self.on_date_selected)
        self.window.action_t_l_ch.triggered.connect(self.switch_to_calendaradd_tab)
        self.window.pushButton_6.clicked.connect(self.switch_to_update_calendar_form)
        self.window.actionXem_l_ch.triggered.connect(self.switch_to_calendar_tab)
        self.window.pushButton_4.clicked.connect(self.delete_calendar_event)
        self.window.pushButton_7.clicked.connect(self.switch_to_physical_tab)
        self.window.btnAddPhysical.clicked.connect(self.add_physical)
        self.window.pushButton_9.clicked.connect(self.refresh_physical)
        self.window.pushButton_10.clicked.connect(self.switch_to_update_physical_form)
        self.window.btnUpdatePhysical.clicked.connect(self.update_physical)
        self.window.pushButton_8.clicked.connect(self.delete_physical)
        self.window.comboBox_6.currentIndexChanged.connect(self.update_chart_for_selected_pet)
        self.window.actionAdd_Pets.triggered.connect(self.switch_to_tab)
        self.window.actionC_p_nh_t_th_ng_tin_v_t_l.triggered.connect(self.switch_to_table_physical_tab)
        self.window.actionBi_u_t_ng_tr_ng.triggered.connect(self.switch_to_chart_tab)
        self.window.pushButton_11.clicked.connect(self.toggle_chart)
        self.window.lineEdit_8.textChanged.connect(self.search_pets)
        self.window.action_ng_xu_t.triggered.connect(self.logout)
    def toggle_chart(self):
        self.is_chart_active = not self.is_chart_active  # Đảo trạng thái
        if self.is_chart_active:
            QMessageBox.information(self.window, "Thông báo", "Biểu đồ đã được bật.")
        else:
            # Xóa biểu đồ hiện tại
            layout = self.window.widget.layout()
            if layout is not None:
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            QMessageBox.information(self.window, "Thông báo", "Biểu đồ đã bị dừng và xóa.")
    def load_calendar(self):
        data = Calendar(self.db_connector,self.user_id).read_all()
        self.calendar_events = data
        self.refresh_calendar()
    
    def load_physical(self):
        data = Physical(self.db_connector, user_id = self.user_id).read_all()
        self.physicals = data
        self.update_physical_table()
    
    
    def load_pets(self):
        data = Pet(self.db_connector, user_id = self.user_id).read_all()
        self.pets = data
        self.update_table()
        
    def switch_to_chart_tab(self):
        self.window.tabWidget.setCurrentIndex(6)
    def switch_to_physical_tab(self):
        self.window.btnAddPhysical.setVisible(True)
        self.window.btnUpdatePhysical.setVisible(False)
        self.window.tabWidget.setCurrentIndex(4)
        self.clear_physical_form()
        
    def switch_to_add_tab(self):
        self.window.tabWidget.setCurrentIndex(1)
        self.clear_form()
    
    def switch_to_calendar_tab(self):
        self.window.tabWidget.setCurrentIndex(2)
        self.refresh_calendar()
    
    def switch_to_table_physical_tab(self):
        self.window.tabWidget.setCurrentIndex(5)
        self.update_physical_table()
    def switch_to_calendaradd_tab(self):
        self.window.btnDatLich.setVisible(True)
        self.window.btnDatLich_2.setVisible(False)
        self.window.tabWidget.setCurrentIndex(3)
        self.clear_calendaradd_form()
    
    def switch_to_tab(self):
        self.window.tabWidget.setCurrentIndex(0)
        self.update_table()
    
    def switch_to_update_tab(self):
        selected_row = self.window.petTable.currentRow()
        if selected_row >= 0:
            self.window.tabWidget.setCurrentIndex(1)
            self.current_form()
        else:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn thú cưng để chỉnh sửa.")

#Physical
    def delete_physical(self):
        selected_row = self.window.petTable_2.currentRow()
        if selected_row >= 0:
            physical = self.physicals[selected_row]
            print(physical)
            physical.delete()
            self.physicals.pop(selected_row)
            self.update_physical_table()
            QMessageBox.information(self.window, "Thành công", "Đã xóa thông tin thể chất.")
        else:
            QMessageBox.warning(self.window, "Lỗi", "Không có thông tin thể chất nào được chọn.")
    def update_physical(self):
        selected_row = self.window.petTable_2.currentRow()
        if selected_row >= 0:
            current_physical = self.physicals[selected_row]

            # Kiểm tra thú cưng được chọn
            pet_id = self.window.comboBox_3.currentData()
            if not pet_id:
                QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn thú cưng.")
                return

            # Kiểm tra cân nặng
            try:
                weight = float(self.window.lineEdit_10.text().strip())
                if weight <= 0 or weight > 200:
                    QMessageBox.warning(self.window, "Lỗi", "Cân nặng phải lớn hơn 0 và nhỏ hơn 200 kg.")
                    return
            except ValueError:
                QMessageBox.warning(self.window, "Lỗi", "Cân nặng phải là số thực.")
                return

            # Kiểm tra chiều cao
            try:
                height = float(self.window.lineEdit_7.text().strip())
                if height <= 0 or height > 300:
                    QMessageBox.warning(self.window, "Lỗi", "Chiều cao phải lớn hơn 0 và nhỏ hơn 300 cm.")
                    return
            except ValueError:
                QMessageBox.warning(self.window, "Lỗi", "Chiều cao phải là số thực.")
                return

            # Kiểm tra ngày
            date = self.window.dateEdit_5.date()
            if date > QDate.currentDate():
                QMessageBox.warning(self.window, "Lỗi", "Ngày kiểm tra không thể trong tương lai.")
                return

            # Kiểm tra xem đã có bản ghi cho ngày này chưa (ngoại trừ bản ghi hiện tại)
            date_str = date.toString("yyyy-MM-dd")
            if any(p.pet_id == pet_id and p.date == date_str and p.physical_id != current_physical.physical_id for p in self.physicals):
                QMessageBox.warning(self.window, "Lỗi", "Đã có bản ghi cho thú cưng này vào ngày này.")
                return

            # Cập nhật thông tin
            current_physical.pet_id = pet_id
            current_physical.pet_name = self.window.comboBox_3.currentText()
            current_physical.weight = weight
            current_physical.height = height
            current_physical.date = date_str
            current_physical.note = self.window.lineEdit_6.text().strip()
            
            current_physical.update()
            self.update_physical_table()
            QMessageBox.information(self.window, "Thành công", "Đã cập nhật thông tin thể chất.")
            self.window.tabWidget.setCurrentIndex(5)  # Chuyển về tab danh sách
        else:
            QMessageBox.warning(self.window, "Lỗi", "Không có thông tin thể chất nào được chọn.")
    def switch_to_update_physical_form(self):
        selected_row = self.window.petTable_2.currentRow()
        if selected_row >= 0:
            self.window.tabWidget.setCurrentIndex(4)
            self.current_physical_form()
        else:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn thông tin thể chất để chỉnh sửa.")
    def current_physical_form(self):
        self.window.btnAddPhysical.setVisible(False)
        self.window.btnUpdatePhysical.setVisible(True)
        selected_row = self.window.petTable_2.currentRow()
        if selected_row >= 0:
            physical = self.physicals[selected_row]
            self.window.comboBox_3.setCurrentText(physical.pet_name)
            self.window.lineEdit_10.setText(str(physical.weight))
            self.window.lineEdit_7.setText(str(physical.height))
            if isinstance(physical.date, datetime.datetime):
                date = physical.date.strftime("%Y-%m-%d")
            else:
                date = physical.date
            self.window.dateEdit_5.setDate(QDate.fromString(date, "yyyy-MM-dd"))
            self.window.lineEdit_6.setText(physical.note)
    
    def refresh_physical(self):
        self.update_physical_table()
        QMessageBox.information(self.window, "Thành công", "Đã tải lại trang thông tin thể chất!")
    def add_physical(self):
        # Kiểm tra thú cưng được chọn
        pet_name = self.window.comboBox_3.currentText()
        pet_id = self.window.comboBox_3.currentData()
        if not pet_id:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn thú cưng.")
            return

        # Kiểm tra cân nặng
        try:
            weight = float(self.window.lineEdit_10.text().strip())
            if weight <= 0 or weight > 200:
                QMessageBox.warning(self.window, "Lỗi", "Cân nặng phải lớn hơn 0 và nhỏ hơn 200 kg.")
                return
        except ValueError:
            QMessageBox.warning(self.window, "Lỗi", "Cân nặng phải là số thực.")
            return

        # Kiểm tra chiều cao
        try:
            height = float(self.window.lineEdit_7.text().strip())
            if height <= 0 or height > 300:
                QMessageBox.warning(self.window, "Lỗi", "Chiều cao phải lớn hơn 0 và nhỏ hơn 300 cm.")
                return
        except ValueError:
            QMessageBox.warning(self.window, "Lỗi", "Chiều cao phải là số thực.")
            return

        # Kiểm tra ngày
        date = self.window.dateEdit_5.date()
        if date > QDate.currentDate():
            QMessageBox.warning(self.window, "Lỗi", "Ngày kiểm tra không thể trong tương lai.")
            return

        # Kiểm tra xem đã có bản ghi cho ngày này chưa
        date_str = date.toString("yyyy-MM-dd")
        if any(p.pet_id == pet_id and p.date == date_str for p in self.physicals):
            QMessageBox.warning(self.window, "Lỗi", "Đã có bản ghi cho thú cưng này vào ngày này.")
            return

        # Tạo bản ghi mới
        new_physical = Physical(
            db=self.db_connector,
            user_id=self.user_id,
            pet_name=pet_name,
            pet_id=pet_id,
            weight=weight,
            height=height,
            date=date_str,
            note=self.window.lineEdit_6.text().strip()
        )
        new_physical.create()
        data = new_physical.get_physical_id()
        self.physicals.append(new_physical)
        self.update_physical_table()
        QMessageBox.information(self.window, "Thành công", "Đã thêm thông tin thể chất.")
        self.clear_physical_form()
    
    def update_physical_table(self):
        self.window.petTable_2.setRowCount(len(self.physicals))
        for row, physical in enumerate(self.physicals):
            self.window.petTable_2.setItem(row, 0, QTableWidgetItem(str(physical.physical_id)))
            self.window.petTable_2.setItem(row, 1, QTableWidgetItem(physical.pet_name))
            self.window.petTable_2.setItem(row, 2, QTableWidgetItem(str(physical.weight)))
            self.window.petTable_2.setItem(row, 3, QTableWidgetItem(str(physical.height)))
            if isinstance(physical.date, datetime.datetime):
                date = physical.date.strftime("%Y-%m-%d")
            else:
                date = physical.date
            self.window.petTable_2.setItem(row, 4, QTableWidgetItem(date))
            self.window.petTable_2.setItem(row, 5, QTableWidgetItem(physical.note))

    def clear_calendaradd_form(self):
        self.populate_pet_combobox()
        pet_name = self.window.comboBox_4.setCurrentIndex(0)
        event = self.window.lineEdit_11.clear()
        event_type = self.window.comboBox_5.setCurrentIndex(0)
        note = self.window.lineEdit_14.clear()
        date = self.window.dateEdit_3.setDate(self.window.dateEdit_3.minimumDate())
        

    def clear_physical_form(self):
        pet_name = self.window.comboBox_3.setCurrentIndex(0)
        weight = self.window.lineEdit_10.clear()
        height = self.window.lineEdit_7.clear()
        date = self.window.dateEdit_5.setDate(self.window.dateEdit_5.minimumDate())
        note = self.window.lineEdit_6.clear()
        


#Celendar
    def delete_calendar_event(self):
    
        date = self.window.calendarWidget.selectedDate()
        date_str = date.toString("yyyy-MM-dd")

        
        matching_events = [
            e for e in self.calendar_events
            if (isinstance(e.date, datetime.datetime) and e.date.strftime("%Y-%m-%d") == date_str) or (e.date == date_str)
        ]

        if not matching_events:
            QMessageBox.warning(self.window, "Lỗi", "Không có sự kiện nào vào ngày được chọn.")
            return

        
        reply = QMessageBox.question(
            self.window,
            "Xác nhận",
            f"Có chắc chắn muốn xóa {len(matching_events)} sự kiện vào ngày {date_str}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            for event in matching_events:
                event.delete()
                self.calendar_events.remove(event)

            self.refresh_calendar()
            QMessageBox.information(self.window, "Thành công", "Đã xóa sự kiện lịch.")

    def switch_to_update_calendar_form(self):
        self.window.btnDatLich.setVisible(False)
        self.window.btnDatLich_2.setVisible(True)
        # Lấy ngày được chọn từ calendarWidget
        date = self.window.calendarWidget.selectedDate()
        date_str = date.toString("yyyy-MM-dd")

        # Tìm các sự kiện khớp với ngày được chọn
        matching_events = []
        for e in self.calendar_events:
            if isinstance(e.date, datetime.datetime):
                if e.date.strftime("%Y-%m-%d") == date_str:
                    matching_events.append(e)
            elif e.date == date_str:
                matching_events.append(e)

        if not matching_events:
            QMessageBox.warning(self.window, "Lỗi", "Không có sự kiện nào vào ngày được chọn.")
            return

        # Nếu có nhiều sự kiện, chọn sự kiện đầu tiên (hoặc tùy chỉnh logic chọn sự kiện)
        event = matching_events[0]
        if isinstance(event.date, datetime.datetime):
            date_str = event.date.strftime("%Y-%m-%d")  # Chuyển datetime thành chuỗi
        else:
            date_str = event.date  # Nếu đã là chuỗi, giữ nguyên



        # Chuyển sang tab "Thêm sự kiện"
        self.window.tabWidget.setCurrentIndex(3)  # Tab "Thêm sự kiện"

        # Điền thông tin sự kiện vào form
        self.window.comboBox_4.setCurrentText(event.pet_name)
        self.window.lineEdit_11.setText(event.event)
        self.window.comboBox_5.setCurrentText(event.event_type)
        self.window.lineEdit_14.setText(event.note)
        self.window.dateEdit_3.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))
        self.window.btnDatLich_2.clicked.connect(lambda: self.update_calendar_event(event))
    
    def update_calendar_event(self,event):
        pet_id = self.window.comboBox_4.currentData()
        event_name = self.window.lineEdit_11.text()
        event_type = self.window.comboBox_5.currentText()
        note = self.window.lineEdit_14.text()
        new_date = self.window.dateEdit_3.date().toString("yyyy-MM-dd")

        # Kiểm tra các trường bắt buộc
        if not pet_id:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn thú cưng.")
            return
        if not event_name:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập tên sự kiện.")
            return
        if not event_type:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn loại sự kiện.")
            return
        if not new_date:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn ngày.")
            return

        event.pet_id = pet_id
        event.event = event_name
        event.event_type = event_type
        event.note = note
        event.date = new_date

        # Gọi phương thức update để lưu thay đổi vào cơ sở dữ liệu
        event.update()
        self.refresh_calendar()  # Làm mới lịch
        self.clear_calendaradd_form()
        QMessageBox.information(self.window, "Thành công", "Đã cập nhật sự kiện lịch.")
        
    def add_calendar_event(self):
        pet_name = self.window.comboBox_4.currentText()
        pet_id = self.window.comboBox_4.currentData()
        event  = self.window.lineEdit_11.text()
        event_type = self.window.comboBox_5.currentText()
        note = self.window.lineEdit_14.text()
        date = self.window.dateEdit_3.date().toString("yyyy-MM-dd")
        if not pet_id:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn thú cưng.")
            return
        if not event:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập tên sự kiện.")
            return
        if not event_type:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn loại sự kiện.")
            return
        if not date:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn ngày.")
            return
        new_event = Calendar(self.db_connector,self.user_id,pet_name,None,pet_id, event_type,event, note, date)
        new_event.create()
        new_event.get_calendar_id()
        self.calendar_events.append(new_event)
        QMessageBox.information(self.window, "Thành công", "Đã thêm sự kiện lịch.")
        
    def on_date_selected(self):
        date = self.window.calendarWidget.selectedDate()
        date_str = date.toString("yyyy-MM-dd")
        matching_events = []
        for e in self.calendar_events:
            if isinstance(e.date, datetime.datetime):
                if e.date.strftime("%Y-%m-%d") == date_str:
                    matching_events.append(e)
            elif e.date == date_str:
                matching_events.append(e)
        if matching_events:
            info = "\n".join([f"🐾 {e.pet_name} - {e.event_type}: {e.note}" for e in matching_events])
            self.window.label_9.setText(info)
        else:
            self.window.label_9.setText("Không có sự kiện nào.")
    
    
    def refresh_calendar(self):
        self.window.calendarWidget.setDateTextFormat(QDate(), QTextCharFormat())  # Clear cũ
        for event in self.calendar_events:
            if isinstance(event.date, datetime.datetime):
                date_str = event.date.strftime("%Y-%m-%d")
            else:
                date_str = event.date
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            fmt = QTextCharFormat()
            fmt.setBackground(QBrush(QColor("#FFE082")))  # Màu cam nhạt
            fmt.setFontWeight(QFont.Bold)
            fmt.setToolTip(f"🐾 {event.pet_name} - {event.event_type}: {event.note}")
            self.window.calendarWidget.setDateTextFormat(qdate, fmt)

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self.window,
            "Chọn ảnh thú cưng",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.current_image_path = file_name
            pixmap = QPixmap(file_name)
            self.window.lblPetImage.setPixmap(pixmap.scaled(
                self.window.lblPetImage.width(),
                self.window.lblPetImage.height(),
                Qt.KeepAspectRatio
            ))

    def clear_form(self):
        self.window.lineEdit.clear()
        self.window.lineEdit_2.clear()
        self.window.lineEdit_3.clear()
        self.window.lineEdit_4.clear()
        self.window.lineEdit_5.clear()
        self.window.comboBox.setCurrentIndex(0)
        self.window.dateEdit.setDate(self.window.dateEdit.minimumDate())
        self.window.lblPetImage.clear()
        self.current_image_path = None
    
    def current_form(self):
        selected_row = self.window.petTable.currentRow()
        if selected_row >= 0:
            pet = self.pets[selected_row]
            self.window.lineEdit.setText(pet.name)
            self.window.lineEdit_2.setText(pet.breed)
            self.window.lineEdit_3.setText(str(pet.age))
            self.window.comboBox.setCurrentText(pet.gender)
            self.window.lineEdit_4.setText(pet.note)
            self.window.lineEdit_5.setText(pet.health_status)
            self.window.dateEdit.setDate(QDate.fromString(pet.adoption_date, "yyyy-MM-dd"))
            self.current_image_path = pet.image_path
            if pet.image_path:
                pixmap = QPixmap(pet.image_path)
                self.window.lblPetImage.setPixmap(pixmap.scaled(
                    self.window.lblPetImage.width(),
                    self.window.lblPetImage.height(),
                    Qt.KeepAspectRatio
            ))
    def update_table(self):
        self.window.petTable.setRowCount(len(self.pets))
        for row, pet in enumerate(self.pets):
            self.window.petTable.setItem(row, 0, QTableWidgetItem(str(pet.id)))
            self.window.petTable.setItem(row, 1, QTableWidgetItem(pet.name))
            self.window.petTable.setItem(row, 2, QTableWidgetItem(pet.breed))
            self.window.petTable.setItem(row, 3, QTableWidgetItem(str(pet.age)))
            self.window.petTable.setItem(row, 4, QTableWidgetItem(pet.gender))
            if isinstance(pet.adoption_date, datetime.datetime):
                date = pet.adoption_date.strftime("%Y-%m-%d")
            else:
                date = pet.adoption_date

            self.window.petTable.setItem(row, 5, QTableWidgetItem(date))
            self.window.petTable.setItem(row, 6, QTableWidgetItem(pet.health_status))
            self.window.petTable.setItem(row, 7, QTableWidgetItem(pet.note))
            
            
            # Hiển thị ảnh nếu có
            if hasattr(pet, 'image_path') and pet.image_path:
                label = QLabel()
                pixmap = QPixmap(pet.image_path)
                label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                label.setAlignment(Qt.AlignCenter)
                self.window.petTable.setCellWidget(row, 8, label)
            else:
                self.window.petTable.setItem(row, 8, QTableWidgetItem("Không có ảnh"))
            
    def add_pet(self):
        # Kiểm tra tên
        new_name = self.window.lineEdit.text().strip()
        if not new_name:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập tên thú cưng.")
            return
        
        # Kiểm tra tên trùng
        if any(pet.name.lower() == new_name.lower() for pet in self.pets):
            QMessageBox.warning(self.window, "Lỗi", f"Thú cưng '{new_name}' đã tồn tại.")
            return

        # Kiểm tra giống
        breed = self.window.lineEdit_2.text().strip()
        if not breed:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập giống thú cưng.")
            return

        # Kiểm tra tuổi
        try:
            age = int(self.window.lineEdit_3.text().strip())
            if age < 0 or age > 100:
                QMessageBox.warning(self.window, "Lỗi", "Tuổi thú cưng phải từ 0 đến 100.")
                return
        except ValueError:
            QMessageBox.warning(self.window, "Lỗi", "Tuổi phải là số nguyên.")
            return

        # Kiểm tra giới tính
        gender = self.window.comboBox.currentText()
        if not gender:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn giới tính thú cưng.")
            return

        # Kiểm tra tình trạng sức khỏe
        health_status = self.window.lineEdit_5.text().strip()
        if not health_status:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập tình trạng sức khỏe.")
            return

        # Kiểm tra ngày nhận nuôi
        adoption_date = self.window.dateEdit.date()
        if adoption_date > QDate.currentDate():
            QMessageBox.warning(self.window, "Lỗi", "Ngày nhận nuôi không thể trong tương lai.")
            return

        # Tạo đối tượng pet mới sau khi đã kiểm tra
        new_pet = Pet(
            db = self.db_connector,
            user_id=self.user_id,
            name=new_name,
            breed=breed,
            age=age,
            gender=gender,
            note=self.window.lineEdit_4.text().strip(),
            adoption_date=adoption_date.toString("yyyy-MM-dd"),
            health_status=health_status,
            image_path=self.current_image_path
        )
        new_pet.create()
        new_pet.get_pet_id()
        self.pets.append(new_pet)
        self.update_table()
        QMessageBox.information(self.window, "Thành công", "Đã thêm thú cưng mới!")
        self.clear_form()
        
    def refresh_pet(self):
        self.update_table()
        QMessageBox.information(self.window, "Thành công", "Đã tải lại trang thông tin thú cưng!")
    
    def update_pet(self):
        selected_row = self.window.petTable.currentRow()
        if selected_row >= 0:
            # Kiểm tra tên
            new_name = self.window.lineEdit.text().strip()
            if not new_name:
                QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập tên thú cưng.")
                return
            
            # Kiểm tra tên trùng (ngoại trừ chính nó)
            current_pet = self.pets[selected_row]
            if any(pet.name.lower() == new_name.lower() and pet.id != current_pet.id for pet in self.pets):
                QMessageBox.warning(self.window, "Lỗi", f"Thú cưng '{new_name}' đã tồn tại.")
                return

            # Kiểm tra giống
            breed = self.window.lineEdit_2.text().strip()
            if not breed:
                QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập giống thú cưng.")
                return

            # Kiểm tra tuổi
            try:
                age = int(self.window.lineEdit_3.text().strip())
                if age < 0 or age > 100:
                    QMessageBox.warning(self.window, "Lỗi", "Tuổi thú cưng phải từ 0 đến 100.")
                    return
            except ValueError:
                QMessageBox.warning(self.window, "Lỗi", "Tuổi phải là số nguyên.")
                return

            # Kiểm tra giới tính
            gender = self.window.comboBox.currentText()
            if not gender:
                QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn giới tính thú cưng.")
                return

            # Kiểm tra tình trạng sức khỏe
            health_status = self.window.lineEdit_5.text().strip()
            if not health_status:
                QMessageBox.warning(self.window, "Lỗi", "Vui lòng nhập tình trạng sức khỏe.")
                return

            # Kiểm tra ngày nhận nuôi
            adoption_date = self.window.dateEdit.date()
            if adoption_date > QDate.currentDate():
                QMessageBox.warning(self.window, "Lỗi", "Ngày nhận nuôi không thể trong tương lai.")
                return

            # Cập nhật thông tin thú cưng
            current_pet.name = new_name
            current_pet.breed = breed
            current_pet.age = age
            current_pet.gender = gender
            current_pet.note = self.window.lineEdit_4.text().strip()
            current_pet.health_status = health_status
            current_pet.adoption_date = adoption_date.toString("yyyy-MM-dd")
            if self.current_image_path:
                current_pet.image_path = self.current_image_path
            
            current_pet.update()
            self.update_table()
            QMessageBox.information(self.window, "Thành công", "Đã cập nhật thông tin thú cưng!")
            self.window.tabWidget.setCurrentIndex(0)  # Chuyển về tab danh sách
        else:
            QMessageBox.warning(self.window, "Lỗi", "Không có thú cưng nào được chọn.")

    def delete_pet(self):
        selected_row = self.window.petTable.currentRow()
        if selected_row >= 0:
            # Logic xóa thú cưng
            pet_id = self.pets[selected_row].id
            pet = Pet(self.db_connector, pet_id)
            pet.delete(pet_id)
            self.pets.pop(selected_row)
            self.update_table()
            QMessageBox.information(self.window, "Thành công", "Đã xóa thú cưng!")
        else:
            QMessageBox.warning(self.window, "Lỗi", "Vui lòng chọn thú cưng cần xóa")
    def logout(self):
        reply = QMessageBox.question(
            self.window,
            "Xác nhận đăng xuất",
            "Bạn có chắc chắn muốn đăng xuất?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Đóng kết nối cơ sở dữ liệu nếu cần
            self.db_connector.close()

            # Import giao diện đăng nhập
            from controller.login_controller import LoginController  # Đảm bảo đường dẫn chính xác
            self.login_window = LoginController("views/Login.ui")  # Lưu đối tượng vào thuộc tính của lớp
            self.login_window.window.show()  # Hiển thị giao diện đăng nhập
            self.window.close()  # Đóng giao diện hiện tại
    def update_chart_for_selected_pet(self):
        if not self.is_chart_active:
            return  # Không làm gì nếu biểu đồ đang bị dừng

        # Lấy pet_id từ comboBox_6
        pet_id = self.window.comboBox_6.currentData()
        if not pet_id:
            QMessageBox.warning(self.window, "Lỗi", "Không tìm thấy thú cưng được chọn.")
            return

        # Lọc dữ liệu liên quan đến thú cưng
        physicals = [p for p in self.physicals if p.pet_id == pet_id]
        if not physicals:
            QMessageBox.warning(self.window, "Lỗi", "Không có dữ liệu để hiển thị biểu đồ.")
            return

        # Chuẩn bị dữ liệu
        dates = [datetime.datetime.strptime(p.date, "%Y-%m-%d") if isinstance(p.date, str) else p.date for p in physicals]
        weights = [float(p.weight) for p in physicals]
        heights = [float(p.height) for p in physicals]

        # Vẽ biểu đồ
        canvas = PlotCanvas(self.window.widget, width=5, height=4)
        canvas.plot(dates, weights, heights)

        # Thêm canvas vào layout
        layout = self.window.widget.layout()
        if layout is None:
            layout = QVBoxLayout(self.window.widget)
            self.window.widget.setLayout(layout)
        else:
            # Xóa các widget cũ trong layout
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        layout.addWidget(canvas)
    def search_pets(self):
        keyword = self.window.lineEdit_8.text().strip().lower()

        if not keyword:
            self.update_table()
            return

        filtered_pets = [
            pet for pet in self.pets
            if keyword in pet.name.lower() or keyword in pet.breed.lower() or keyword in pet.note.lower()
        ]

        self.window.petTable.setRowCount(len(filtered_pets))
        for row, pet in enumerate(filtered_pets):
            self.window.petTable.setItem(row, 0, QTableWidgetItem(str(pet.id)))
            self.window.petTable.setItem(row, 1, QTableWidgetItem(pet.name))
            self.window.petTable.setItem(row, 2, QTableWidgetItem(pet.breed))
            self.window.petTable.setItem(row, 3, QTableWidgetItem(str(pet.age)))
            self.window.petTable.setItem(row, 4, QTableWidgetItem(pet.gender))
            if isinstance(pet.adoption_date, datetime.datetime):
                date = pet.adoption_date.strftime("%Y-%m-%d")
            else:
                date = pet.adoption_date
            self.window.petTable.setItem(row, 5, QTableWidgetItem(date))
            self.window.petTable.setItem(row, 6, QTableWidgetItem(pet.health_status))
            self.window.petTable.setItem(row, 7, QTableWidgetItem(pet.note))

            if hasattr(pet, 'image_path') and pet.image_path:
                label = QLabel()
                pixmap = QPixmap(pet.image_path)
                label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                label.setAlignment(Qt.AlignCenter)
                self.window.petTable.setCellWidget(row, 8, label)
            else:
                self.window.petTable.setItem(row, 8, QTableWidgetItem("Không có ảnh"))