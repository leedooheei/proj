import socket
import json
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QGridLayout, QApplication, QFrame


class AdminDisplay(QWidget):
    def __init__(self, username=None, orders=None):
        super().__init__()
        self.setWindowTitle("관리자 화면")
        self.setGeometry(0, 0, 1024, 600)
        self.username = username
        self.orders = orders

        self.grid_layout = QGridLayout()

        # 현재 시간과 날짜를 표시할 Label
        self.current_time_label = QLabel()
        self.grid_layout.addWidget(self.current_time_label, 0, 5, 1, 1)  # 오른쪽 위에 위치 조정
        self.update_time()

        # 주기적으로 시간을 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1초마다 업데이트

        # 주문 목록 레이블 추가
        self.order_label = QLabel("주문 목록")
        self.order_layout = QVBoxLayout()
        self.order_layout.addWidget(self.order_label)

        # 그리드를 6칸으로 나누고, 선으로 구분
        for i in range(2):
            for j in range(3):
                frame = QFrame()
                frame.setFrameShape(QFrame.Box)
                frame.setFrameShadow(QFrame.Raised)
                frame.setLineWidth(2)
                self.grid_layout.addWidget(frame, i+1, j, 1, 1)

        self.grid_layout.addLayout(self.order_layout, 1, 1, 1, 1)  # 주문 목록이 더 큰 공간을 차지하도록 조정

        self.setLayout(self.grid_layout)

        self.client_thread = ClientThread()
        self.client_thread.order_received.connect(self.display_order_info)
        self.client_thread.start()

    def display_order_info(self, order_info_json):
        order_info = json.loads(order_info_json)
        order_number = order_info['order_number']
        total_price = order_info['total_price']
        eat_where = order_info['EatWhere']
        cart = order_info['cart']

        order_details = f"Order #{order_number}\nTotal Price: {total_price}\nEat Where: {eat_where}\nItems:\n"
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


class ClientThread(QThread):
    order_received = pyqtSignal(str)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(("127.0.0.1", 12345))
            while True:
                data = client_socket.recv(1024).decode("utf-8")
                if data:
                    self.order_received.emit(data)


if __name__ == "__main__":
    import sys

    def main():
        app = QApplication(sys.argv)
        display = AdminDisplay()
        display.show()
        sys.exit(app.exec_())

    main()
