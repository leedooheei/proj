import sys
import json
import mysql.connector
import pyttsx3
import requests
import decimal
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog
from PyQt5.QtGui import QIcon


class PaymentScreen(QDialog):
    payment_completed = pyqtSignal(float)
    counter_order_requested = pyqtSignal()
    def __init__(self, username, cart, EatWhere=None, order_number=None,menu_data = None, parent=None):
        super().__init__(parent)
        self.username = username
        self.setWindowTitle("키오스크 결제 화면")
        self.setGeometry(100, 100, 480, 800)
        self.font_size = 16
        self.menu_data = menu_data
        self.selected_payment = None
        self.cart = cart
        self.order_number = order_number
        self.EatWhere = EatWhere
        self.selected_payment_button = None
        self.initUI()
        print("메뉴 데이터 유형:", type(self.menu_data)) 

    def set_cart(self, cart):
        self.cart = list(cart)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(100, self.activate_voice_guide)

    def activate_voice_guide(self):
        self.speak_instruction("결제 방법을 선택하세요.")

    def speak_instruction(self, instruction):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(instruction)
        engine.runAndWait()

    def initUI(self):
        self.back_button = QPushButton("이전", self)
        self.back_button.setFixedSize(100, 50)
        self.back_button.setStyleSheet("font-size: 20px;")
        self.back_button.clicked.connect(self.back_button_clicked)

        self.font_increase_button = QPushButton("+", self)
        self.font_increase_button.clicked.connect(self.increase_font_size)
        self.font_increase_button.setFixedSize(50, 50)

        self.font_decrease_button = QPushButton("-", self)
        self.font_decrease_button.clicked.connect(self.decrease_font_size)
        self.font_decrease_button.setFixedSize(50, 50)

        self.menu_info_label = QLabel(self)
        self.menu_info_label.setStyleSheet("font-size: 12pt;")
        self.display_menu_info()

        font_button_layout = QHBoxLayout()
        font_button_layout.addWidget(self.font_increase_button)
        font_button_layout.addWidget(self.font_decrease_button)
        font_button_layout.setAlignment(Qt.AlignRight)

        self.label = QLabel("\n\n결제수단을 선택하세요\n", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            "color: orange; font-family: 'Black Han Sans', sans-serif; font-weight: 400; font-size: {}pt; text-align: "
            "center;".format(self.font_size))

        self.card_payment_button = QPushButton("카드결제", self)
        self.card_payment_button.setIcon(QIcon("pic/card_icon.png"))
        self.card_payment_button.setIconSize(QSize(120, 160))
        self.card_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.card_payment_button.clicked.connect(self.select_card_payment)

        self.counter_payment_button = QPushButton("카운터에서 결제", self)
        self.counter_payment_button.setIcon(QIcon("pic/counter_icon.png"))
        self.counter_payment_button.setIconSize(QSize(120, 160))
        self.counter_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.counter_payment_button.clicked.connect(self.select_counter_payment)

        self.select_button = QPushButton("선택", self)
        self.select_button.setStyleSheet(
            "background-color: orange; color: white; font-size: 16pt; border-radius: 20px;")
        self.select_button.clicked.connect(self.process_selection)
        self.select_button.setFixedSize(300, 50)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.card_payment_button)
        button_layout.addWidget(self.counter_payment_button)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.back_button)
        top_layout.addLayout(font_button_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.label, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.menu_info_label, alignment=Qt.AlignHCenter)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.select_button, alignment=Qt.AlignHCenter)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

        self.update_font()

    def back_button_clicked(self):
        self.close()
        from MainWindow import VoiceKiosk
        self.voice_kiosk = VoiceKiosk(self.username)
        self.voice_kiosk.show()

    def increase_font_size(self):
        self.font_size += 2
        self.update_font()

    def decrease_font_size(self):
        self.font_size -= 2
        self.update_font()

    def update_font(self):
        self.label.setStyleSheet(
            "color: orange; font-family: 'Black Han Sans', sans-serif; font-weight: 400; font-size: {}pt; "
            "text-align: center;".format(self.font_size))
        self.card_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.counter_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.menu_info_label.setStyleSheet(
            "font-size: {}pt;".format(self.font_size))

    def select_card_payment(self):
        self.selected_payment = "카드결제"
        self.card_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: orange;".format(self.font_size))
        self.counter_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))

    def select_counter_payment(self):
        self.selected_payment = "카운터에서 결제"
        self.card_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.counter_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: orange;".format(self.font_size))

    def process_selection(self):
        if self.selected_payment is None:
            QMessageBox.warning(self, "경고", "결제 방식을 선택해주세요.")
        else:
            from MainWindow import OrderNumberManager
            order_number_manager = OrderNumberManager()
            order_number = order_number_manager.generate_order_number()
            self.payment_screen = PaymentScreen(self.username, self.cart, self.EatWhere, order_number)
            self.payment_screen.payment_completed.connect(self.handle_payment_completed)
            self.hide()
            self.payment_screen.show()

    def process_payment(self, payment_method):
        from MainWindow import OrderNumberManager
        order_number_manager = OrderNumberManager()
        order_number = order_number_manager.generate_order_number()

        total_price = sum(float(item['price']) * float(item['quantity']) for item in self.cart)

        order_details = {
            'order_number': order_number,
            'cart': self.cart,
            'eat_where': self.EatWhere,
            'payment_method': payment_method,
            'total_price': total_price
        }

        try:
            save_order_to_db(self.username, order_details['order_number'],
                             order_details['total_price'], order_details['eat_where'], order_details['cart'])
            send_order_to_server(order_details)
        except Exception as e:
            QMessageBox.warning(self, "오류 발생", f"주문 처리 중 오류 발생: {str(e)}")
        else:
            QMessageBox.information(self, "주문 완료", "주문이 성공적으로 저장되었습니다.")
            self.go_mainWindow()
    def go_mainWindow(self):
        from MainWindow import MainWindow
        self.main_window = MainWindow(self.username)
        self.close()
        self.main_window.show()

    def display_menu_info(self):
        menu_info = "메뉴 정보:\n"
        for item in self.cart:
            if isinstance(item, dict):
                menu_info += f" - {item['name']} - 가격: {item['price']}원, 수량: {item['quantity']}개\n"
            else:
                pass
        self.menu_info_label.setText(menu_info)


def send_order_to_server(order_details):
    url = 'http://localhost:5000/orders'
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    print("Sending order details to server:", order_details)

    try:
        response = requests.post(url, json=order_details, headers=headers)
        if response.status_code == 200:
            print('주문 정보가 성공적으로 전송되었습니다.')
        else:
            print(f'주문 정보 전송 실패: {response.status_code}, {response.text}')
    except requests.exceptions.RequestException as e:
        print(f'주문 정보 전송 요청 실패: {e}')

    except Exception as e:
        print(f'주문 정보 전송 요청 실패: {e}')


def save_order_to_db(username, order_number, total_price, eat_where, items):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO menu_order (username, order_number, total_price, eat_where, items)
        VALUES (%s, %s, %s, %s, %s)
        """
        items_json = json.dumps(items, default=lambda x: float(x) if isinstance(x, decimal.Decimal) else None)
        cursor.execute(insert_query, (username, order_number, total_price, eat_where, items_json))

        connection.commit()
        QMessageBox.information(None, "저장 성공", "주문이 성공적으로 저장되었습니다.")

    except mysql.connector.Error as e:
        QMessageBox.warning(None, "오류 발생", f"MySQL 오류 발생: {str(e)}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    username = "user"
    cart = []
    EatWhere = "none"
    order_number = "1234"  # 주문 번호
    window = PaymentScreen(username=username, cart=cart, EatWhere=EatWhere, order_number=order_number)
    window.show()
    sys.exit(app.exec_())
