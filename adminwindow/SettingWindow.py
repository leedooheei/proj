import sys
from functools import partial

import mysql.connector
import json
from PyQt5.QtCore import QDate, Qt, QTime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QApplication, QLabel, QTextEdit, QDateEdit, QListWidget, QListWidgetItem, QMenu, QTableWidget,
    QTableWidgetItem
)

class SalesAggregateWindow(QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("판매집계")
        self.setGeometry(100, 100, 800, 600)  # 테이블 크기 조정
        self.username = username
        self.current_date = QDate.currentDate()
        self.order_number = 0  # 주문번호 초기화

        self.init_ui()
        self.load_sales_data()
        self.order_table.itemClicked.connect(self.display_order_details)  # 주문 테이블의 아이템 클릭 시그널 연결

    def init_ui(self):
        layout = QVBoxLayout()

        # 날짜 선택 부분
        date_layout = QHBoxLayout()
        self.prev_date_button = QPushButton("< 전날")
        self.prev_date_button.clicked.connect(self.load_prev_date)

        self.date_edit = QDateEdit(self.current_date)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.dateChanged.connect(self.load_sales_data)

        self.next_date_button = QPushButton("다음날 >")
        self.next_date_button.clicked.connect(self.load_next_date)

        date_layout.addWidget(self.prev_date_button)
        date_layout.addWidget(self.date_edit)
        date_layout.addWidget(self.next_date_button)

        layout.addLayout(date_layout)

        # 주문 내역 테이블
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(6)  # 주문번호 추가
        self.order_table.setHorizontalHeaderLabels(["주문번호", "주문시간", "총가격", "결제방식", "주문내역","주문취소"])
        layout.addWidget(self.order_table)

        # 주문 상세 보기
        self.order_details = QTextEdit()
        self.order_details.setReadOnly(True)
        layout.addWidget(self.order_details)

        # 페이지 업/다운 버튼
        page_layout = QHBoxLayout()
        self.page_up_button = QPushButton("▲ 페이지 업")
        self.page_up_button.clicked.connect(self.page_up)
        self.page_down_button = QPushButton("▼ 페이지 다운")
        self.page_down_button.clicked.connect(self.page_down)
        page_layout.addWidget(self.page_up_button)
        page_layout.addWidget(self.page_down_button)
        layout.addLayout(page_layout)

        # 총 매출 정보
        self.total_sales_label = QLabel()
        self.card_sales_label = QLabel()
        self.counter_sales_label = QLabel()

        layout.addWidget(self.total_sales_label)
        layout.addWidget(self.card_sales_label)
        layout.addWidget(self.counter_sales_label)

        self.setLayout(layout)

    def get_order_details(self, order_id):
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="kiosk"
            )
            cursor = db_connection.cursor()

            query = """
                SELECT id, total_price, eat_where, created_at, items
                FROM menu_order
                WHERE id = %s
            """

            cursor.execute(query, (order_id,))
            order = cursor.fetchone()

            if order:
                _, total_price, eat_where, created_at, items = order

                # 주문 세부 정보 생성
                order_details = f"주문 시간: {created_at}\n총 가격: {total_price}\n결제 방식: {eat_where}\n\n"

                # 주문 내역에 대한 정보 추출 및 추가
                items = json.loads(items)
                for index, item in enumerate(items, start=1):
                    name = item['name']
                    price = item['price']
                    quantity = item.get('quantity', 1)
                    order_details += f"{index}. {name}: {price}원 x {quantity}\n"

                return order_details
            else:
                return None

        except mysql.connector.Error as e:
            print("MySQL 오류:", e)
            return None
        finally:
            if db_connection is not None and db_connection.is_connected():
                cursor.close()
                db_connection.close()

    def load_sales_data(self):
        self.order_table.clearContents()  # 기존 내용 삭제
        total_sales = 0

        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="kiosk"
            )
            cursor = db_connection.cursor()
            selected_date = self.current_date.toString("yyyy-MM-dd")

            query = """
                SELECT id, total_price, eat_where, created_at, items
                FROM menu_order
                WHERE username = %s AND DATE(created_at) = %s
                ORDER BY created_at desc # 오래된 주문부터 가져오도록 변경
            """

            cursor.execute(query, (self.username, selected_date))
            orders = cursor.fetchall()

            self.order_table.setRowCount(len(orders))  # 행 개수 설정

            # 주문번호를 오래된 순으로 1부터 시작하도록 초기화
            order_number = len(orders)


            for row, order in enumerate(orders):
                _, total_price, eat_where, created_at, items = order
                total_sales += total_price

                # 숫자로만 데이터 표시
                order_number_item = QTableWidgetItem(str(order_number))
                self.order_table.setItem(row, 0, order_number_item)

                # 시간만 표시
                created_at_time = QTime.fromString(created_at.strftime("%H:%M:%S"), "hh:mm:ss")
                created_at_item = QTableWidgetItem(created_at_time.toString("hh:mm"))
                self.order_table.setItem(row, 1, created_at_item)

                total_price_item = QTableWidgetItem(f"{total_price:.2f}")
                self.order_table.setItem(row, 2, total_price_item)

                # 결제 방식 표시
                payment_method_item = QTableWidgetItem(eat_where)
                self.order_table.setItem(row, 3, payment_method_item)

                # 주문 내역 표시
                items_text = ""
                for item in json.loads(items):
                    items_text += f"{item['name']}: {item['price']}원\n"
                items_item = QTableWidgetItem(items_text)
                self.order_table.setItem(row, 4, items_item)

                order_number -= 1  # 오래된 주문부터 1씩 감소시킴


                cancel_button = QPushButton("주문 취소")
                cancel_button.clicked.connect(partial(self.cancel_order, id))
                self.order_table.setCellWidget(row, 5, cancel_button)  # 버튼 추가

            self.total_sales_label.setText(f"총 판매 금액: {total_sales:.2f}원")

        except mysql.connector.Error as e:
            print("MySQL 오류:", e)
        finally:
            if db_connection is not None and db_connection.is_connected():
                cursor.close()
                db_connection.close()

    def display_order_details(self, item):
        row = item.row()  # 클릭된 아이템의 행 인덱스 가져오기
        order_id = int(self.order_table.item(row, 0).text())  # 주문번호 대신 ID 사용

        # 데이터베이스에서 주문 세부 정보 가져오기
        order_details = self.get_order_details(order_id)

        if order_details:
            # 주문 세부 정보를 텍스트 에디터에 표시
            self.order_details.setText(order_details)
        else:
            # 주문 데이터가 없는 경우 메시지 출력
            self.order_details.setText("주문 상세 정보를 가져올 수 없습니다.")

    def page_up(self):
        self.order_table.verticalScrollBar().triggerAction(self.order_table.verticalScrollBar().SliderPageStepSub)

    def page_down(self):
        self.order_table.verticalScrollBar().triggerAction(self.order_table.verticalScrollBar().SliderPageStepAdd)

    def load_prev_date(self):
        self.current_date = self.current_date.addDays(-1)
        self.date_edit.setDate(self.current_date)
        self.load_sales_data()

    def load_next_date(self):
        self.current_date = self.current_date.addDays(1)
        self.date_edit.setDate(self.current_date)
        self.load_sales_data()

    def cancel_order(self, order_id):
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="kiosk"
            )
            cursor = db_connection.cursor()

            query = "SELECT eat_where FROM menu_order WHERE id = %s"
            cursor.execute(query, (order_id,))
            eat_where = cursor.fetchone()

            if eat_where == 'counter':
                # 카운터 결제인 경우 처리
                # 금액 차감 로직을 여기에 추가하세요
                query = "DELETE FROM menu_order WHERE id = %s"
                cursor.execute(query, (order_id,))
                db_connection.commit()
                QMessageBox.information(self, "성공", "카운터 결제 주문이 취소되었습니다.")
            else:
                # 카드 결제인 경우 처리
                pass

        except mysql.connector.Error as e:
            print("MySQL 오류:", e)
        finally:
            if db_connection.is_connected():
                cursor.close()
                db_connection.close()


    def contextMenuEvent(self, event):
        menu = QMenu(self)
        cancel_action = menu.addAction("주문 취소")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == cancel_action:
            selected_item = self.order_table.currentItem()
            if selected_item:
                order = selected_item.data(Qt.UserRole)
                order_id = order[0]  # Assuming order_id is the first element of the order tuple
                self.cancel_order(order_id)


class ChangePasswordWindow(QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("비밀번호 변경")
        self.setGeometry(100, 100, 300, 200)
        self.username = username
        layout = QVBoxLayout()

        self.current_password_input = QLineEdit()
        self.current_password_input.setPlaceholderText("현재 비밀번호")
        self.current_password_input.setEchoMode(QLineEdit.Password)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("새로운 비밀번호 (4자리)")
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("새로운 비밀번호 확인 (4자리)")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

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

        # 새로운 비밀번호가 4자리인지 확인
        if len(new_password) != 4:
            QMessageBox.warning(self, "경고", "새로운 비밀번호는 4자리여야 합니다.")
            return

        # 새로운 비밀번호 확인이 4자리인지 확인
        if len(confirm_password) != 4:
            QMessageBox.warning(self, "경고", "새로운 비밀번호 확인은 4자리여야 합니다.")
            return

        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )
        cursor = db_connection.cursor()

        try:
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

            if new_password != confirm_password:
                QMessageBox.warning(self, "경고", "새 비밀번호가 일치하지 않습니다.")
                return

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

        self.exit_button = QPushButton("나가기", self)
        self.exit_button.clicked.connect(self.go_close)

        main_layout.addWidget(self.sales_aggregate_button)
        main_layout.addWidget(self.change_manager_key_button)
        main_layout.addWidget(self.exit_button)
        self.setLayout(main_layout)

    def go_close(self):
        from Admin_Function import AdminFunctionWindow
        AdminMain_Window = AdminFunctionWindow()
        AdminMain_Window.show()
        self.close()

    def show_sales_aggregate(self):
        self.sales_aggregate_window = SalesAggregateWindow(self.username)
        self.sales_aggregate_window.exec_()

    def open_change_password_window(self):
        change_password_window = ChangePasswordWindow(self.username)
        if change_password_window.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "성공", "비밀번호가 성공적으로 변경되었습니다.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    username = "user"
    display = SettingWindow(username=username)
    display.show()
    sys.exit(app.exec_())
