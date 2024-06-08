import sys
import mysql.connector
import json
from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QGridLayout, QApplication, QFrame, QMessageBox


class AdminDisplay(QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.setWindowTitle("관리자 화면")
        self.setGeometry(0, 0, 1024, 600)
        self.username = username
        self.order_layout = QVBoxLayout()
        self.init_ui()

        # 주문 목록을 가져오는 타이머 설정
        self.polling_timer = QTimer(self)
        self.polling_timer.timeout.connect(self.poll_orders)
        self.polling_timer.start(5000)  # 5초마다 데이터베이스를 폴링

    def init_ui(self):
        # 현재 시간과 날짜를 표시할 Label
        self.current_time_label = QLabel()
        self.update_time()
        self.order_layout.addWidget(self.current_time_label)

        # 주문 목록 레이블 추가
        self.order_label = QLabel("주문 목록")
        self.order_layout.addWidget(self.order_label)

        self.setLayout(self.order_layout)

    def poll_orders(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="kiosk"
            )
            cursor = connection.cursor()
            query = "SELECT * FROM menu_order ORDER BY created_at DESC"
            cursor.execute(query)
            orders = cursor.fetchall()

            for order in orders:
                order_id, order_number, total_price, eat_where, items, created_at = order
                if order_id not in self.displayed_order_ids:
                    self.displayed_order_ids.add(order_id)
                    order_info = {
                        "order_number": order_number,
                        "total_price": total_price,
                        "EatWhere": eat_where,
                        "cart": json.loads(items),
                        "created_at": created_at
                    }
                    self.display_order_info(order_info)

        except mysql.connector.Error as e:
            print("MySQL 오류:", e)
            QMessageBox.critical(self, "Database Error", f"MySQL 오류: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_ui_with_new_order(self, order_info):
        order_number = order_info['order_number']
        total_price = order_info['total_price']
        eat_where = order_info['EatWhere']
        cart = order_info['cart']
        created_at = order_info['created_at']

        order_details = f"Order #{order_number}\nTotal Price: {total_price}\nEat Where: {eat_where}\nOrder Time: {created_at}\nItems:\n"
        for item in cart:
            name = item['name']
            price = item['price']
            quantity = item.get('quantity', 1)
            order_details += f"  - {name}: {price}원 x {quantity}\n"

        order_label = QLabel(order_details)
        self.order_layout.addWidget(order_label)

    def update_time(self):
        current_time = QDateTime.currentDateTime()
        self.current_time_label.setText(current_time.toString("yyyy-MM-dd hh:mm:ss"))

if __name__ == "__main__":
    def main():
        app = QApplication(sys.argv)
        username = "admin"
        display = AdminDisplay(username)
        display.show()
        sys.exit(app.exec_())

    main()
