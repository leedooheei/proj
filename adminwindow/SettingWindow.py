import sys
import json
import mysql.connector
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication, QDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QDateEdit, QMenu
)
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
        self.exit_button.clicked.connect(self.close_window)

        main_layout.addWidget(self.sales_aggregate_button)
        main_layout.addWidget(self.change_manager_key_button)
        main_layout.addWidget(self.exit_button)
        self.setLayout(main_layout)

    def close_window(self):
        self.close()

    def show_sales_aggregate(self):
        self.sales_aggregate_window = SalesAggregateWindow(self.username)
        self.sales_aggregate_window.exec_()

    def open_change_password_window(self):
        change_password_window = ChangePasswordWindow(self.username)
        if change_password_window.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "성공", "비밀번호가 성공적으로 변경되었습니다.")

class SalesAggregateWindow(QDialog):
    def __init__(self, username=None):
        super().__init__()
        self.setWindowTitle("판매집계")
        self.setGeometry(100, 100, 800, 600)
        self.username = username
        self.current_date = QDate.currentDate()
        self.order_number = 0  # 주문번호 초기화

        self.init_ui()
        self.load_sales_data()
        self.order_table.itemClicked.connect(self.display_order_details)

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
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(["주문번호", "주문시간", "총가격", "매장/포장", "주문내역", "주문취소"])
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

    def load_sales_data(self):
        self.order_table.clearContents()
        total_sales = 0
        total_counter_sales = 0
        total_card_sales = 0
        self.order_number = 0  # 날짜마다 주문번호 초기화

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
                  ORDER BY created_at DESC
              """

            cursor.execute(query, (self.username, selected_date))
            orders = cursor.fetchall()

            self.order_table.setRowCount(len(orders))

            for row, order in enumerate(orders):
                order_id, total_price, payment_method, created_at, items = order
                total_sales += total_price
                self.order_number += 1  # 주문번호 증가


                if payment_method == '카운터에서 결제':
                    total_counter_sales += total_price
                elif payment_method == '카드결제':
                    total_card_sales += total_price

                order_number_item = QTableWidgetItem(str(self.order_number))  # 수정된 부분
                self.order_table.setItem(row, 0, order_number_item)

                created_at_time = QTime.fromString(created_at.strftime("%H:%M:%S"), "hh:mm:ss")
                created_at_item = QTableWidgetItem(created_at_time.toString("hh:mm"))
                self.order_table.setItem(row, 1, created_at_item)

                total_price_item = QTableWidgetItem(f"{total_price:.2f}원")
                self.order_table.setItem(row, 2, total_price_item)

                payment_method_item = QTableWidgetItem(payment_method)
                self.order_table.setItem(row, 3, payment_method_item)

                items_text = ""
                for item in json.loads(items):
                    items_text += f"{item['name']}: {item['price']}원\n"
                items_item = QTableWidgetItem(items_text)
                self.order_table.setItem(row, 4, items_item)

                cancel_button = QPushButton("주문 취소")
                cancel_button.clicked.connect(lambda _, oid=order_id: self.cancel_order(oid))
                self.order_table.setCellWidget(row, 5, cancel_button)

            self.total_sales_label.setText(f"총 판매 금액: {total_sales:.2f}원")
            self.card_sales_label.setText(f"카드 결제 총 금액: {total_card_sales:.2f}원")
            self.counter_sales_label.setText(f"카운터 결제 총 금액: {total_counter_sales:.2f}원")

        except mysql.connector.Error as e:
            print("MySQL 오류:", e)
            QMessageBox.critical(self, "에러", "데이터베이스 연결 중 오류 발생.")

        finally:
            if 'db_connection' in locals():
                if db_connection.is_connected():
                    cursor.close()
                    db_connection.close()

    def display_order_details(self, item):
        row = item.row()
        order_id = int(self.order_table.item(row, 0).text())

        order_details = self.get_order_details(order_id)

        if order_details:
            self.order_details.setText(order_details)
        else:
            self.order_details.setText("주문 상세 정보를 가져올 수 없습니다.")

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
                order_id, total_price, eat_where, created_at, items = order

                details = f"주문번호: {order_id}\n"
                details += f"주문시간: {created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                details += f"총가격: {total_price:.2f}원\n"
                details += f"매장/포장: {eat_where}\n"
                details += "주문내역:\n"
                for item in json.loads(items):
                    details += f"  - {item['name']}: {item['price']}원\n"

                return details

        except mysql.connector.Error as e:
            print("MySQL 오류:", e)
            QMessageBox.critical(self, "에러", "데이터베이스 연결 중 오류 발생.")

        finally:
            if 'db_connection' in locals():
                if db_connection.is_connected():
                    cursor.close()
                    db_connection.close()

        return None

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

            # 주문 정보를 가져옵니다
            query = "SELECT total_price, payment_method FROM menu_order WHERE id = %s"
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()

            if result:
                total_price, payment_method = result

                # 주문을 삭제합니다
                delete_query = "DELETE FROM menu_order WHERE id = %s"
                cursor.execute(delete_query, (order_id,))
                db_connection.commit()

                if payment_method == 'counter':
                    current_counter_sales = float(self.counter_sales_label.text().split(": ")[1].replace("원", ""))
                    updated_counter_sales = current_counter_sales - float(total_price)
                    self.counter_sales_label.setText(f"카운터 결제 총 금액: {updated_counter_sales:.2f}원")
                elif payment_method == 'card':
                    current_card_sales = float(self.card_sales_label.text().split(": ")[1].replace("원", ""))
                    updated_card_sales = current_card_sales - float(total_price)
                    self.card_sales_label.setText(f"카드 결제 총 금액: {updated_card_sales:.2f}원")

                current_total_sales = float(self.total_sales_label.text().split(": ")[1].replace("원", ""))
                updated_total_sales = current_total_sales - float(total_price)
                self.total_sales_label.setText(f"총 판매 금액: {updated_total_sales:.2f}원")

                # 테이블에서 해당 주문의 상태를 "취소완료"로 변경하고 색상을 빨간색으로 변경
                for row in range(self.order_table.rowCount()):
                    if int(self.order_table.item(row, 0).text()) == order_id:
                        cancel_complete_item = QTableWidgetItem("취소완료")
                        cancel_complete_item.setForeground(QColor("red"))
                        self.order_table.setItem(row, 5, cancel_complete_item)
                        break

                QMessageBox.information(self, "성공", "주문이 성공적으로 취소되었습니다.")
                self.load_sales_data()

            else:
                QMessageBox.warning(self, "경고", "주문을 찾을 수 없습니다.")

        except mysql.connector.Error as e:
            print("MySQL 오류:", e)
            QMessageBox.critical(self, "에러", "주문 취소 중 오류 발생.")

        finally:
            if 'db_connection' in locals():
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
                order_id = int(self.order_table.item(selected_item.row(), 0).text())
                self.cancel_order(order_id)


class ChangePasswordWindow(QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("비밀번호 변경")
        self.setGeometry(200, 200, 300, 150)

        self.username = username

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.password_label = QLabel("새 비밀번호:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_label = QLabel("새 비밀번호 확인:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.change_password_button = QPushButton("비밀번호 변경")
        self.change_password_button.clicked.connect(self.change_password)

        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.change_password_button)

        self.setLayout(layout)

    def change_password(self):
        new_password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if new_password != confirm_password:
            QMessageBox.warning(self, "경고", "새 비밀번호와 확인 비밀번호가 일치하지 않습니다.")
            return

        if len(new_password) < 8:
            QMessageBox.warning(self, "경고", "새 비밀번호는 최소 8자 이상이어야 합니다.")
            return

        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="kiosk"
            )
            cursor = db_connection.cursor()

            query = "UPDATE users SET password = %s WHERE username = %s"
            cursor.execute(query, (new_password, self.username))
            db_connection.commit()

            QMessageBox.information(self, "성공", "비밀번호가 성공적으로 변경되었습니다.")

            self.password_input.clear()
            self.confirm_password_input.clear()

        except mysql.connector.Error as e:
            print("MySQL 오류:", e)
            QMessageBox.critical(self, "에러", "비밀번호 변경 중 오류 발생.")

        finally:
            if 'db_connection' in locals() and db_connection.is_connected():
                cursor.close()
                db_connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    username = "qwer1"  # 테스트용 사용자 이름
    sales_window = SalesAggregateWindow(username)
    sales_window.show()

    change_password_window = ChangePasswordWindow(username)
    change_password_window.show()

    sys.exit(app.exec_())

