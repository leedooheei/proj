import decimal
import json
import socket
from decimal import Decimal

import mysql.connector
import pyttsx3
import sys

import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, \
    QGridLayout, QTabWidget, QMessageBox


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

    def __init__(self, username=None, menu_data=None, EatWhere=None):
        super(NormalWindow, self).__init__()
        self.username = username  # Initialize username attribute
        self.menu_data = menu_data
        self.cart = [] # 메뉴 데이터를 처리하여 장바구니에 저장

        self.voice_thread = VoiceThread()
        self.voice_thread.start()

        self.EatWhere = EatWhere
        self.initUI()

    def process_menu_data(self):
        # menu_data를 처리하여 장바구니 리스트를 반환
        cart_items = []
        for menu_list in self.menu_data.values():
            for menu in menu_list:
                cart_items.append(menu)
        return cart_items

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
            # 장바구니에 담긴 상품들을 콘솔에 출력
            print("장바구니에 담긴 상품들:")
            for item in self.cart:
                print(f"{item['name']} - 가격: {item['price']}원")

            try:
                if not isinstance(self.username, str):
                    raise ValueError("사용자 이름이 문자열이 아닙니다.")
                if not isinstance(self.EatWhere, str):
                    raise ValueError("식사 장소 정보가 문자열이 아닙니다.")

                self.payment_screen = PaymentScreen(self.username, self.cart, self.EatWhere)
                self.payment_screen.payment_completed.connect(self.handle_payment_completed)
                self.hide()
                self.payment_screen.show()
            except ValueError as ve:
                print(f"오류 발생: {ve}")
            except Exception as e:
                print("기타 오류 발생:", e)
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

            item_label = QLabel(f"{item['name']} - 가격: {str(item['price'])}원")
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

    def handle_payment_completed(self, total_price):
        order_number_manager = OrderNumberManager()
        order_number = order_number_manager.generate_order_number()

        order_details = {
            'order_number': order_number,
            'cart': self.cart,
            'total_price': total_price,
            'EatWhere': self.EatWhere,
            'payment_method': self.payment_screen.payment_method
        }

        save_order_to_db(self.username, order_details['order_number'], order_details['total_price'],
                         order_details['EatWhere'], order_details['payment_method'], self.cart)

        send_order_to_server(order_details)

        self.cart = []
        self.update_cart_view()
        self.update_total_price()
        self.show_normal_window()


        self.return_to_main_window()



import requests



def send_order_to_server(order_details):
    url = 'http://localhost:5000/orders'
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    for item in order_details['cart']:
        item['price'] = float(item['price'])  # Decimal을 float로 변환

    try:
        response = requests.post(url, json=order_details, headers=headers)
        if response.status_code == 200:
            print('주문 정보가 성공적으로 전송되었습니다.')
        else:
            print(f'주문 정보 전송 실패: {response.status_code}, {response.text}')
    except Exception as e:
        print(f'주문 정보 전송 요청 실패: {e}')



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


class PaymentScreen(QWidget):
    payment_completed = pyqtSignal(float)
    counter_order_requested = pyqtSignal()

    def __init__(self, username, cart, EatWhere=None, parent=None):
        super().__init__(parent)
        self.username = username  # 사용자 이름을 저장
        self.setWindowTitle("키오스크 결제 화면")
        self.setGeometry(100, 100, 480, 800)
        self.font_size = 16
        self.selected_payment = None
        self.cart = cart  # 장바구니 정보 전달
        self.EatWhere = EatWhere  # MainWindow에서 전달된 EatWhere 값을 사용
        self.selected_payment_button = None  # 선택된 결제 버튼을 나타내는 변수
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
        self.card_payment_button.setIcon(QIcon("pic/card_icon.png"))
        self.card_payment_button.setIconSize(QSize(120, 160))
        self.card_payment_button.setStyleSheet("font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
        self.card_payment_button.clicked.connect(self.select_card_payment)


        self.counter_payment_button = QPushButton("카운터에서 결제", self)
        self.counter_payment_button.setIcon(QIcon("pic/counter_icon.png"))
        self.counter_payment_button.setIconSize(QSize(120, 160))
        self.counter_payment_button.setStyleSheet("font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))
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
        self.orderMain = NormalWindow(self.username
                                      )
        self.orderMain.show()

    def select_card_payment(self):
        self.selected_payment = "카드결제"
        self.update_selected_button_style(self.card_payment_button)

    def select_counter_payment(self):
        self.selected_payment = "카운터에서 결제"
        self.update_selected_button_style(self.counter_payment_button)

    def update_selected_button_style(self, button):
        # 이전에 선택된 버튼이 있으면 해당 버튼의 스타일을 초기화
        if self.selected_payment_button:
            self.selected_payment_button.setStyleSheet(
                "font-size: {}pt; height: 200px; background-color: white;".format(self.font_size))

        # 선택된 버튼에 새로운 스타일 적용
        button.setStyleSheet("font-size: {}pt; height: 200px; background-color: orange;".format(self.font_size))
        self.selected_payment_button = button

    def process_selection(self):
        if self.selected_payment is None:
            QMessageBox.warning(self, "경고", "결제 방식을 선택해주세요.")
        else:
            self.payment_method = self.selected_payment  # 선택된 결제 방법 저장
            if self.selected_payment == "카드결제":
                # 카드 결제 처리 코드
                print("장바구니에 담긴 상품들:", self.cart)
                print(self.EatWhere)
                order_number_manager = OrderNumberManager()
                order_number = order_number_manager.generate_order_number()
                order_details = {
                    'order_number': order_number,
                    'cart': self.cart,
                    'total_price': float(sum(item['price'] * item.get('quantity', 1) for item in self.cart)),
                    'EatWhere': self.EatWhere,
                    'payment_method': self.payment_method  # 추가
                }

                save_order_to_db(self.username, order_details['order_number'], order_details['total_price'],
                                 order_details['EatWhere'], order_details['payment_method'], self.cart)

                print("카드결제 화면으로 이동합니다.")
                self.complete_payment()

            elif self.selected_payment == "카운터에서 결제":
                # 카운터 결제 처리 코드
                print("장바구니에 담긴 상품들:", self.cart)
                print(self.EatWhere)
                order_number_manager = OrderNumberManager()
                order_number = order_number_manager.generate_order_number()
                order_details = {
                    'order_number': order_number,
                    'cart': self.cart,
                    'total_price': float(sum(item['price'] * item.get('quantity', 1) for item in self.cart)),
                    'EatWhere': self.EatWhere,
                    'payment_method': self.payment_method  # 추가
                }

                save_order_to_db(self.username, order_details['order_number'], order_details['total_price'],
                                 order_details['EatWhere'], order_details['payment_method'], self.cart)

                # 주문 정보를 소켓을 통해 전송
                send_order_to_server(order_details)

                # 메인 창으로 돌아가기
                self.complete_payment()

    def complete_payment(self):
        from MainWindow import MainWindow
        self.main_window = MainWindow(self.username)

        self.main_window.show()
        self.close()
def get_menu_data_from_database(username):
    menu_data = {}
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )
        if db:
            cursor = db.cursor(dictionary=True)
            # 사용자가 주문한 메뉴 데이터만 가져오도록 WHERE 절 추가
            cursor.execute("SELECT name, price, category, image FROM menu WHERE username = %s", (username,))
            rows = cursor.fetchall()
            for row in rows:
                name = row["name"]
                price = row["price"]
                category = row["category"]
                image = row["image"]
                if category not in menu_data:
                    menu_data[category] = []
                menu_data[category].append({"name": name, "price": price, "image": image})
            cursor.close()
            db.close()
    except mysql.connector.Error as e:
        pass
    return menu_data
def save_order_to_db(username, order_number, total_price, eat_where, payment_method, items):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )
        cursor = connection.cursor()

        # 주문 정보 저장
        insert_order_query = """
        INSERT INTO menu_order (username, order_number, total_price, eat_where, payment_method)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_order_query, (username, order_number, total_price, eat_where, payment_method))
        order_id = cursor.lastrowid  # 방금 삽입한 주문의 ID 가져오기

        # 각 항목을 order_items 테이블에 저장
        insert_item_query = """
        INSERT INTO order_items (order_id, item_name, item_price, item_quantity)
        VALUES (%s, %s, %s, %s)
        """
        for item in items:
            item_name = item['name']
            item_price = item['price']
            item_quantity = item.get('quantity', 1)
            cursor.execute(insert_item_query, (order_id, item_name, item_price, item_quantity))

        connection.commit()

    except mysql.connector.Error as e:
        print("MySQL 오류:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




if __name__ == "__main__":
    app = QApplication([])
    username = "user"
    menu_data = get_menu_data_from_database(username=username)
    main_window = NormalWindow(menu_data)
    main_window.show()
    sys.exit(app.exec_())
