import socket
import mysql.connector
import pyttsx3
import sys

import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QGridLayout, QTabWidget
class VoiceThread(QThread):
    speak_completed = pyqtSignal()
    def __init__(self, parent=None):
        super(VoiceThread, self).__init__(parent)
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', 'english+f3')
        self.text_to_speak = None

    def run(self):
        if self.text_to_speak:
            self.engine.say(self.text_to_speak)
            self.engine.runAndWait()
            self.speak_completed.emit()

    def speak(self, text):
        self.text_to_speak = text
        self.start()

    def stop(self):
        self.stop_thread = True

class OrderNumberManager:
    def __init__(self):
        self.current_order_number = 1

    def generate_order_number(self):
        order_number = self.current_order_number
        self.current_order_number += 1
        return order_number

    def reset_order_number(self):
        self.current_order_number = 1

class NormalWindow(QMainWindow):
    def __init__(self, menu_data):
        super(NormalWindow, self).__init__()
        self.menu_data = menu_data
        self.voice_thread = VoiceThread()
        self.voice_thread.start()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("키오스크")
        self.setFixedSize(800, 600)
        self.cart = []  # 장바구니 정보를 저장할 리스트

        main_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        for category, menus in self.menu_data.items():
            category_widget = QWidget()
            category_layout = QVBoxLayout()
            category_widget.setLayout(category_layout)
            tab_widget.addTab(category_widget, category)

            # 탭마다 그리드 레이아웃 생성 및 설정
            grid_layout = QGridLayout()
            category_layout.addLayout(grid_layout)

            # 각 메뉴 버튼을 그리드에 추가
            for i, menu in enumerate(menus):
                menu_button_text = "{}\n가격: {}원".format(menu['name'], menu['price'])
                menu_button = QPushButton(menu_button_text)
                menu_button.setStyleSheet("font-size: 20px; padding: 20px;")
                menu_button.clicked.connect(lambda _, m=menu: self.add_to_cart(m))

                # 그리드에 메뉴 버튼을 추가
                row = i // 3  # 행 인덱스
                column = i % 3  # 열 인덱스
                grid_layout.addWidget(menu_button, row, column)

        self.cart_widget = QWidget()
        cart_layout = QVBoxLayout()
        self.cart_widget.setLayout(cart_layout)

        self.cart_label = QLabel("장바구니")
        cart_layout.addWidget(self.cart_label)

        self.cart_item_layout = QVBoxLayout()
        cart_layout.addLayout(self.cart_item_layout)

        main_layout.addWidget(self.cart_widget)

        payment_button = QPushButton("결제하기")
        payment_button.setStyleSheet("font-size: 30px; padding: 20px;")
        payment_button.clicked.connect(self.go_to_payment)
        main_layout.addWidget(payment_button)

        self.total_price_label = QLabel()
        self.update_total_price()
        main_layout.addWidget(self.total_price_label)

        self.show()

    def update_total_price(self):
        total_price = sum(item['price'] * item.get('quantity', 1) for item in self.cart)
        self.total_price_label.setText(f"총 합계: {total_price}원")

    def go_to_payment(self):
        if not self.cart:
            self.play_order_no()
        else:
            try:
                self.payment_screen = PaymentScreen(self.cart)
                self.payment_screen.payment_completed.connect(self.handle_payment_completed)
                self.hide()
                self.payment_screen.show()

            except Exception as e:
                print("오류 발생:", e)
                sys.exit(1)

    def handle_counter_order_requested(self):
        # 카운터 주문 요청 시 처리할 내용 추가
        self.cart = []  # 장바구니 비우기
        self.show_normal_window()

    def show_normal_window(self):
        self.show()

    def play_order_menu_guide(self):
        self.voice_thread.speak("주문하실 메뉴를 선택해주세요.")

    def play_order_no(self):
        self.voice_thread.speak("장바구니가 비어 있습니다.")
    def play_menu_name(self, menu_name):
        self.voice_thread.speak(menu_name)

    def add_to_cart(self, menu):
        existing_item = next((item for item in self.cart if item['name'] == menu['name']), None)
        if existing_item:
            existing_item['quantity'] += 1
        else:
            menu_copy = menu.copy()
            menu_copy['quantity'] = 1
            self.cart.append(menu_copy)

        self.update_cart_view()  # 장바구니 뷰 업데이트
        self.update_total_price()  # 총 가격 업데이트
        self.play_menu_name(menu['name'])
        # 장바구니 뷰 업데이트
    def update_cart_view(self):
        for i in reversed(range(self.cart_item_layout.count())):
            self.cart_item_layout.itemAt(i).widget().setParent(None)

        for item in self.cart:
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            item_widget.setLayout(item_layout)

            item_label = QLabel(f"{item['name']} - 가격: {item['price']}원")
            item_layout.addWidget(item_label)

            quantity_label = QLabel("수량:")
            item_layout.addWidget(quantity_label)

            quantity_value_label = QLabel(str(item.get('quantity', 1)))
            item_layout.addWidget(quantity_value_label)

            plus_button = QPushButton("+")
            plus_button.clicked.connect(lambda _, m=item: self.increase_quantity(m))
            item_layout.addWidget(plus_button)

            minus_button = QPushButton("-")
            minus_button.clicked.connect(lambda _, m=item: self.decrease_quantity(m))
            item_layout.addWidget(minus_button)

            remove_button = QPushButton("삭제")
            remove_button.clicked.connect(lambda _, m=item: self.remove_from_cart(m))
            item_layout.addWidget(remove_button)

            self.cart_item_layout.addWidget(item_widget)

# 총 가격 업데이트
    def update_total_price(self):
        total_price = sum(item['price'] * item.get('quantity', 1) for item in self.cart)
        self.total_price_label.setText(f"총 합계: {total_price}원")

    def increase_quantity(self, menu):
        menu['quantity'] += 1
        self.update_cart_view()
        self.update_total_price()

    def decrease_quantity(self, menu):
        if menu['quantity'] > 1:
            menu['quantity'] -= 1
            self.update_cart_view()
            self.update_total_price()

    def remove_from_cart(self, menu):
        self.cart.remove(menu)
        self.update_cart_view()  # 장바구니 뷰 업데이트
        self.update_total_price()  # 총 가격 업데이트

    def handle_payment_completed(self, total_price):
        order_number = "1234"  # 주문번호는 임의의 값으로 설정
        menu_names = ", ".join(item['name'] for item in self.cart)
        payment_time = "12:00"  # 결제 시간은 임의의 값으로 설정

        # 주문 정보를 관리자 디스플레이어로 전송
        # self.send_order_info_to_admin(order_number, menu_names, payment_time)

        # 결제 완료 후 장바구니 비우기
        self.cart = []
        self.update_cart_view()
        self.update_total_price()
        self.show_normal_window()

class PaymentScreen(QWidget):
    payment_completed = pyqtSignal(float)
    counter_order_requested = pyqtSignal()

    def __init__(self, cart):
        super().__init__()
        self.setWindowTitle("키오스크 결제 화면")
        self.setGeometry(100, 100, 480, 800)
        self.font_size = 16
        self.selected_payment = None
        self.cart = cart

        self.initUI()

    def initUI(self):

        self.back_button = QPushButton("이전", self)
        self.back_button.setFixedSize(100, 50)
        self.back_button.setStyleSheet("font-size: 20px;")
        self.back_button.clicked.connect(self.back_button_clicked)


        self.label = QLabel("\n\n결제수단을 선택하세요\n", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            "color: orange; font-family: 'Black Han Sans', sans-serif; font-weight: 400; font-size: {}pt; text-align: center;".format(
                self.font_size))


        self.card_payment_button = QPushButton("카드결제", self)
        self.card_payment_button.setStyleSheet(
            "font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.card_payment_button.clicked.connect(self.select_card_payment)


        self.counter_payment_button = QPushButton("카운터에서 주문", self)
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

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.label, alignment=Qt.AlignHCenter)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.select_button, alignment=Qt.AlignHCenter)
        main_layout.addStretch(1)

    def back_button_clicked(self):
        self.close()

    def select_card_payment(self):
        self.selected_payment = "카드결제"
        print("카드 결제 선택됨:", self.selected_payment)
        self.process_selection()

    def select_counter_payment(self):
        self.selected_payment = "카운터에서 주문"
        print("카운터 결제 선택됨:", self.selected_payment)
        self.process_selection()

    def process_selection(self):
        if self.selected_payment:
            print("선택한 결제 방법:", self.selected_payment)
            if self.selected_payment == "카드결제":
                total_price = sum(item['price'] * item.get('quantity', 1) for item in self.cart)
                self.payment_completed.emit(total_price)
            elif self.selected_payment == "카운터에서 주문":
                self.counter_order_requested.emit()
        else:
            print("결제 방법을 먼저 선택하세요.")


def get_menu_data_from_database():
    menu_data = {}
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )
        if db:
            print("데이터베이스 연결 성공!")
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT name, price, category FROM menu")
            rows = cursor.fetchall()
            print("데이터를 가져왔습니다:")
            for row in rows:
                print(row)
                name = row["name"]
                price = row["price"]
                category = row["category"]
                if category not in menu_data:
                    menu_data[category] = []
                menu_data[category].append({"name": name, "price": price})
            cursor.close()
            db.close()
    except mysql.connector.Error as e:
        print(f"데이터베이스 연결 실패: {str(e)}")
    return menu_data


if __name__ == "__main__":
    app = QApplication([])
    menu_data = get_menu_data_from_database()
    main_window = NormalWindow(menu_data)
    main_window.show()
    sys.exit(app.exec_())