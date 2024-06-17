import sys
import json
import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea

class AdminDisplay(QWidget):
    server_url = 'http://localhost:5000/orders'


    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.orders = []
        self.current_start_index = 0
        self.init_ui()
        self.fetch_orders()
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_orders)
        self.timer.start(2000)  # 2초마다 데이터 업데이트


    def init_ui(self):
        self.setWindowTitle('Admin Display')
        self.resize(800, 600)
        self.layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.orders_widget = QWidget()
        self.orders_layout = QVBoxLayout(self.orders_widget)

        self.scroll_area.setWidget(self.orders_widget)
        self.layout.addWidget(self.scroll_area)

        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("이전")
        self.next_button = QPushButton("다음")
        self.prev_button.clicked.connect(self.show_previous_orders)
        self.next_button.clicked.connect(self.show_next_orders)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def fetch_orders(self):
        try:
            response = requests.get(self.server_url)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
            self.orders = response.json()
            self.display_orders()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching orders: {e}")

    def display_orders(self):
        for i in reversed(range(self.orders_layout.count())):
            self.orders_layout.itemAt(i).widget().deleteLater()

        for order in self.orders[self.current_start_index:self.current_start_index + 10]:
            order_number = order['order_number']
            EatWhere = order['EatWhere']
            payment_method = order['payment_method']
            order_time = order.get('order_time', 'N/A')

            order_info = f"Order Number: {order_number}\n"
            order_info += f"Eat Where: {EatWhere}\n"
            order_info += f"Payment Method: {payment_method}\n"
            order_info += f"Order Time: {order_time}\n"
            order_info += "Items:\n"
            for item in order['cart']:
                item_name = item['name']
                item_quantity = item.get('quantity', 1)
                order_info += f"    - {item_name}, Quantity: {item_quantity}\n"

            label = QLabel(order_info)
            label.setWordWrap(True)

            self.orders_layout.addWidget(label)



    def show_previous_orders(self):
        if self.current_start_index > 0:
            self.current_start_index -= 10
            self.display_orders()

    def show_next_orders(self):
        if self.current_start_index + 10 < len(self.orders):
            self.current_start_index += 10
            self.display_orders()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_display = AdminDisplay()
    admin_display.show()
    sys.exit(app.exec_())
