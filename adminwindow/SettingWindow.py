import sys

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QApplication


class SettingWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("환경 설정")
        self.setGeometry(100, 100, 400, 300)
        main_layout = QVBoxLayout()
        self.sales_aggregate_button = QPushButton("판매집계", self)
        self.sales_aggregate_button.clicked.connect(self.show_sales_aggregate)

        self.change_manager_key_button = QPushButton("관리자비밀번호\n 변경", self)
        self.change_manager_key_button.clicked.connect(self.change_manager_key)

        self.prepare_for_business_button = QPushButton("영업 준비", self)
        self.prepare_for_business_button.clicked.connect(self.prepare_for_business)

        self.close_sales_button = QPushButton("판매 마감", self)
        self.close_sales_button.clicked.connect(self.close_sales)

        self.exit_button = QPushButton("나가기", self)
        self.exit_button.clicked.connect(self.go_close)

        main_layout.addWidget(self.sales_aggregate_button)
        main_layout.addWidget(self.change_manager_key_button)
        main_layout.addWidget(self.prepare_for_business_button)
        main_layout.addWidget(self.close_sales_button)
        main_layout.addWidget(self.exit_button)  # Add the exit button
        self.setLayout(main_layout)

    def go_close(self):
        from Admin_Main import AdminMainWindow
        AdminMain_Window = AdminMainWindow()
        AdminMain_Window.show()


    def show_sales_aggregate(self):
        # Implement functionality to show sales aggregate by date
        pass

    def change_manager_key(self):
        # Implement functionality to change manager's key
        pass

    def prepare_for_business(self):
        # Implement functionality to reset order numbers
        pass

    def close_sales(self):
        # Implement functionality to save sales data for the day
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingWindow()
    window.show()
    sys.exit(app.exec_())

