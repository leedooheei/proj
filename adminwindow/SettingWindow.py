import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QApplication, QLabel
)


class ChangePasswordWindow(QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("비밀번호 변경")
        self.setGeometry(100, 100, 300, 200)
        self.username = username
        layout = QVBoxLayout()

        self.current_password_input = QLineEdit()
        self.current_password_input.setPlaceholderText("현재 비밀번호")

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("새로운 비밀번호")

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("새로운 비밀번호 확인")

        self.change_button = QPushButton("변경하기")
        self.change_button.clicked.connect(self.confirm_change)

        layout.addWidget(self.current_password_input)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.change_button)

        self.setLayout(layout)

    def confirm_change(self):
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        # 데이터베이스 연결
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )
        cursor = db_connection.cursor()

        try:
            # 기존 비밀번호 확인
            query = "SELECT managerkey FROM users WHERE username = %s"
            cursor.execute(query, (self.username,))
            result = cursor.fetchone()
            if result:
                stored_password = result[0]
                if stored_password != current_password:
                    QMessageBox.warning(self, "경고", "현재 비밀번호가 일치하지 않습니다.")
                    return
            else:
                QMessageBox.warning(self, "경고", "사용자를 찾을 수 없습니다.")
                return

            # 새 비밀번호 확인
            if new_password != confirm_password:
                QMessageBox.warning(self, "경고", "새 비밀번호가 일치하지 않습니다.")
                return

            # 기존 비밀번호와 새 비밀번호가 일치하면 데이터베이스 업데이트
            query = "UPDATE users SET managerkey = %s WHERE username = %s"
            cursor.execute(query, (new_password, self.username))
            db_connection.commit()
            QMessageBox.information(self, "성공", "비밀번호가 성공적으로 변경되었습니다.")
            self.accept()
        except mysql.connector.Error as err:
            print("에러:", err)
            QMessageBox.critical(self, "에러", "비밀번호 변경 중 오류 발생.")
        finally:
            cursor.close()
            db_connection.close()

        # 여기에 데이터베이스 연결 및 비밀번호 변경 로직 추가
        self.accept()

class SettingWindow(QDialog):
    def __init__(self, username=None):
        super().__init__()
        self.setWindowTitle("환경 설정")
        self.setGeometry(100, 100, 400, 300)
        self.username = username

        main_layout = QVBoxLayout()

        self.sales_aggregate_button = QPushButton("판매집계", self)
        self.sales_aggregate_button.clicked.connect(self.show_sales_aggregate)

        self.change_manager_key_button = QPushButton("비밀번호 변경", self)
        self.change_manager_key_button.clicked.connect(self.open_change_password_window)

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
        main_layout.addWidget(self.exit_button)
        self.setLayout(main_layout)

    def go_close(self):
        from Admin_Main import AdminMainWindow
        AdminMain_Window = AdminMainWindow()
        AdminMain_Window.show()

    def show_sales_aggregate(self):
        # Implement functionality to show sales aggregate by date
        pass

    def prepare_for_business(self):
        pass

    def open_change_password_window(self):
        # Change this line to pass the username when creating ChangePasswordWindow
        change_password_window = ChangePasswordWindow(self.username)
        if change_password_window.exec_() == QDialog.Accepted:
            # Change password logic
            QMessageBox.information(self, "성공", "비밀번호가 성공적으로 변경되었습니다.")

    def close_sales(self):  # Add this method
        # Implement functionality to close sales
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingWindow()
    window.show()
    sys.exit(app.exec_())
