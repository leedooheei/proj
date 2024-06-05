import mysql.connector
import re
import sys
import socket

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QRadioButton, QMessageBox, \
    QMainWindow, QWidget, QApplication
from PyQt5.QtCore import QSize


class AdminWindow(QMainWindow):
    def __init__(self, order_number):
        super().__init__()
        self.order_number = order_number  # 초기 주문 번호 설정
        self.setWindowTitle("관리자 화면")
        self.setGeometry(480, 800)
        self.initUI()#메인 첫 화면
import importlib
import sys
import time

import mysql.connector
import pyttsx3
import speech_recognition as sr
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

 # Normal.py 파일에서 NormalWindow 클래스 import
# from Recommend import MenuWidget

class MainWindow(QMainWindow):
    def go_manager(self):
        from adminwindow.Admin_Main import AdminMainWindow
        self.manager_window = AdminMainWindow(username=self.username)
        self.manager_window.show()

    def __init__(self, username=None):
        from LoginWindow import LoginWindow
        super(MainWindow, self).__init__()
        self.setStyleSheet(u"Background-color:rgb(255, 255, 255);")
        self.setFixedSize(480, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.login_window = LoginWindow()  # LoginWindow 인스턴스 생성
        self.username = username
        self.MainDisplay = QWidget()
        self.MainDisplay.setObjectName(u"MainDisplay")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainDisplay.sizePolicy().hasHeightForWidth())
        self.MainDisplay.setSizePolicy(sizePolicy)
        self.MainDisplay.setFixedSize(480, 800)
        self.MainStackWidget = QStackedWidget(self.MainDisplay)
        self.MainStackWidget.setObjectName(u"MainStackWidget")
        self.MainStackWidget.setGeometry(QRect(0, 0, 480, 800))
        self.EatWhere = ""

        # 전체 큰 화면 위젯(메인)
        self.PagePlaceNMethod = QWidget()
        self.PagePlaceNMethod.setObjectName(u"PagePlaceNMethod")
        self.verticalLayoutWidget = QWidget(self.PagePlaceNMethod)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 480, 800))
        self.LayoutPlaceNMethod = QVBoxLayout(self.verticalLayoutWidget)
        self.LayoutPlaceNMethod.setObjectName(u"LayoutPlaceNMethod")
        self.LayoutPlaceNMethod.setContentsMargins(0, 0, 0, 0)
        self.LayoutWelcomeNSize = QHBoxLayout()
        self.LayoutWelcomeNSize.setObjectName(u"LayoutWelcomeNSize")
        self.LayoutSetting = QVBoxLayout()
        self.LayoutSetting.setObjectName(u"LayoutSetting")

        # 세팅버튼 및 홈버튼 정의
        self.SettingButton = QPushButton(self.verticalLayoutWidget)
        icon = QIcon()
        icon.addFile(u":/AdminSetup/settings.png", QSize(), QIcon.Normal, QIcon.On)
        self.SettingButton.setIcon(icon)
        self.SettingButton.setIconSize(QSize(20, 20))
        self.SettingButton.setFixedSize(30, 30)
        self.SettingButton.setFlat(1)

        self.ButtonHome = QPushButton(self.verticalLayoutWidget)
        iconBack = QIcon()
        iconBack.addFile(u":img/AdminSetup/left.png", QSize(), QIcon.Normal, QIcon.On)
        self.ButtonHome.setIcon(iconBack)
        self.ButtonHome.setFixedSize(50, 30)

        # 관리자 설정 진입하는 버튼 배치
        self.LayoutSetting.addWidget(self.SettingButton)
        self.LayoutSetting.addWidget(self.ButtonHome)

        # 세팅버튼 클릭시 관리자 페이지 호출
        self.SettingButton.clicked.connect(self.go_manager)
        # 홈버튼 클릭시 홈화면으로 복귀
        self.ButtonHome.clicked.connect(self.go_home)

        self.LabelWelcome = QLabel(self.verticalLayoutWidget)
        self.LabelWelcome.setObjectName(u"LabelWelcome")
        font = QFont()
        font.setFamily(u"학교안심 우주 R")
        font.setPointSize(25)
        self.LabelWelcome.setFont(font)
        self.LabelWelcome.setAlignment(Qt.AlignCenter)
        self.LabelWelcome.setMaximumSize(320, 100)
        self.LabelWelcome.setText("쉽고 간편하게\n주문하세요")

        self.VlayoutTextsize = QVBoxLayout()
        self.LabelTextsize = QLabel(self.verticalLayoutWidget)
        self.LabelTextsize.setFont(font)
        self.LabelTextsize.setAlignment(Qt.AlignCenter)
        self.LabelTextsize.setText("글씨 크기")

        self.VlayoutTextsize.addWidget(self.LabelTextsize)

        self.LayoutSizebutton = QHBoxLayout()
        self.LayoutSizebutton.setObjectName(u"LayoutSizebutton")
        self.ButtonBig = QPushButton(self.verticalLayoutWidget)
        self.ButtonBig.setObjectName(u"ButtonBig")
        self.ButtonBig.setFixedSize(62, 62)
        sizemodifyfont = QFont()
        sizemodifyfont.setFamily(u"Noto Sans CJK KR Bold")
        sizemodifyfont.setPointSize(40)
        self.ButtonBig.setFont(sizemodifyfont)
        self.ButtonBig.setStyleSheet(u"border-radius:15px;\n"
                                     "border: 2px solid rgb(45, 45, 45);\n""color: rgb(255,127,0)")

        self.LayoutSizebutton.addWidget(self.ButtonBig)

        self.ButtonSmall = QPushButton(self.verticalLayoutWidget)
        self.ButtonSmall.setObjectName(u"ButtonSmall")
        self.ButtonSmall.setFont(sizemodifyfont)
        self.ButtonSmall.setStyleSheet(u"border-radius:15px;\n"
                                       "border: 2px solid rgb(45, 45, 45);\n""color: rgb(255,127,0)")
        self.ButtonSmall.setFixedSize(62, 62)
        self.ButtonBig.setText("+")
        self.ButtonSmall.setText("−")
        # 레이아웃 중첩배치 및 레이아웃 사이 공간 추가
        self.LayoutSizebutton.addWidget(self.ButtonSmall)
        self.VlayoutTextsize.addLayout(self.LayoutSizebutton)
        self.LayoutWelcomeNSize.addLayout(self.LayoutSetting)
        self.LayoutWelcomeNSize.addStretch(1)
        self.LayoutWelcomeNSize.addWidget(self.LabelWelcome)
        self.LayoutWelcomeNSize.addStretch(1)
        self.LayoutWelcomeNSize.addLayout(self.VlayoutTextsize)

        self.LayoutPlaceNMethod.addLayout(self.LayoutWelcomeNSize)

        self.SWidgetPlaceNMethod = QStackedWidget(self.verticalLayoutWidget)
        self.SWidgetPlaceNMethod.setObjectName(u"SWidgetPlaceNMethod")
        self.PageSelectWhere = QWidget()
        self.PageSelectWhere.setObjectName(u"PageSelectWhere")
        self.verticalLayoutWidget_2 = QWidget(self.PageSelectWhere)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 480, 690))
        self.VLayoutSelectWhere = QVBoxLayout(self.verticalLayoutWidget_2)
        self.VLayoutSelectWhere.setObjectName(u"VLayoutSelectWhere")
        self.VLayoutSelectWhere.setContentsMargins(0, 0, 0, 0)
        self.LabelSelectWhere = QLabel(self.verticalLayoutWidget_2)
        self.LabelSelectWhere.setObjectName(u"LabelSelectWhere")
        self.LabelSelectWhere.setFont(font)
        self.LabelSelectWhere.setMaximumSize(480, 40)
        self.LabelSelectWhere.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.LabelSelectWhere.setText("식사 장소를 선택하세요")
        self.VLayoutSelectWhere.addWidget(self.LabelSelectWhere)

        self.LayoutWhereButton = QHBoxLayout()
        self.LayoutWhereButton.setObjectName(u"LayoutWhereButton")

        def BtnWhere(filename, text):
            btn = QPushButton()
            btn.setStyleSheet(f"QPushButton {{ background-image: url('img/Here&ToGo/{filename}');"
                              f"background-position: center; background-repeat: no-repeat; background-size: contain; }}")
            btn.setMaximumSize(220, 600)
            btn.setFlat(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setText(text)
            btn.clicked.connect(self.go_method)
            return btn

        self.BtnHere = BtnWhere("Eat_Here.png", "먹고가기")  # 먹고가기 버튼 디자인 정의
        self.BtnTake = BtnWhere("Take_Out.png", "포장하기")  # 테이크아웃 버튼 디자인 정의

        # 버튼을 배치
        self.LayoutWhereButton.addWidget(self.BtnHere)
        self.LayoutWhereButton.addWidget(self.BtnTake)

        self.VLayoutSelectWhere.addLayout(self.LayoutWhereButton)

        self.SWidgetPlaceNMethod.addWidget(self.PageSelectWhere)
        self.PageOrdermethod = QWidget()
        self.gridLayoutWidget = QWidget(self.PageOrdermethod)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 480, 690))
        self.LayoutOrdermethod = QGridLayout(self.gridLayoutWidget)
        self.LayoutOrdermethod.setObjectName(u"LayoutOrdermethod")
        self.LayoutOrdermethod.setContentsMargins(0, 0, 0, 0)

        def makeOrderBtn(text, wid, hei):
            # 버튼 생성을 함수로 정의(생성될 레이아웃,가로,세로 크기)
            btn = QPushButton()
            btn.setFont(font)
            btn.setStyleSheet(u"border-radius:15px; border: 2px solid rgb(45, 45, 45);")
            btn.setText(text)
            btn.setFixedSize(wid, hei)
            return btn

        self.BtnChoboOdr = makeOrderBtn("쉬운 주문하기", 470, 180)  # 초보용 주문 버튼 설정
        self.BtnRecOdr = makeOrderBtn("메뉴 추천", 470, 180)  # 메뉴 추천 버튼 설정
        self.BtnVoiceOdr = makeOrderBtn("음성 주문", 470, 180)  # 음성 주문 버튼 설정

        # 주문 버튼 배치
        self.LayoutOrdermethod.addWidget(self.BtnChoboOdr, 1, 0)
        self.LayoutOrdermethod.addWidget(self.BtnVoiceOdr, 2, 0)
        self.LayoutOrdermethod.addWidget(self.BtnRecOdr, 3, 0)

        # 각 주문별 버튼입력 시 페이지 전환
        self.BtnChoboOdr.clicked.connect(self.go_normal_order)
        self.BtnVoiceOdr.clicked.connect(self.go_voice)
        self.BtnRecOdr.clicked.connect(self.go_recommend)

        self.LabelMethodSelect = QLabel(self.gridLayoutWidget)
        self.LabelMethodSelect.setObjectName(u"LabelMethodSelect")
        self.LabelMethodSelect.setFont(font)
        self.LabelMethodSelect.setAlignment(Qt.AlignCenter)
        self.LabelMethodSelect.setText("주문 방법을 선택하세요")

        self.LayoutOrdermethod.addWidget(self.LabelMethodSelect, 0, 0)
        self.SWidgetPlaceNMethod.addWidget(self.PageOrdermethod)
        self.LayoutPlaceNMethod.addWidget(self.SWidgetPlaceNMethod)


        self.MainStackWidget.addWidget(self.PagePlaceNMethod)



        self.setCentralWidget(self.MainDisplay)

        self.SWidgetPlaceNMethod.setCurrentIndex(0)
        # 버튼에 기능 연결
        self.ButtonBig.clicked.connect(self.increase_font_size)
        self.ButtonSmall.clicked.connect(self.decrease_font_size)

        # 글꼴 크기 초기값 설정
        self.font_size = 25



    # 글씨 크기 늘리는 함수
    def increase_font_size(self):
        self.font_size += 1
        self.update_font()

    # 글씨 크기 줄이는 함수
    def decrease_font_size(self):
        self.font_size -= 1
        self.update_font()

    # 변경된 글씨 크기를 업데이트 시켜주는 함수
    def update_font(self):
        font = QFont()
        font.setFamily("학교안심 우주 R")
        font.setPointSize(self.font_size)
        self.LabelWelcome.setFont(font)
        self.LabelSelectWhere.setFont(font)
        self.LabelMethodSelect.setFont(font)
        self.BtnVoiceOdr.setFont(font)
        self.BtnRecOdr.setFont(font)
        self.BtnChoboOdr.setFont(font)

    def go_method(self):
        # 페이지 넘기는 함수
        self.SWidgetPlaceNMethod.setCurrentWidget(self.PageOrdermethod)

    def go_home(self):
        # 홈으로 보내는 함수
        self.MainStackWidget.setCurrentIndex(0)
        self.SWidgetPlaceNMethod.setCurrentIndex(0)
        self.EatWhere = ""

    def go_normal_order(self):
        from Normal import NormalWindow, get_menu_data_from_database
        self.close()
        menu_data = get_menu_data_from_database()
        self.normal_window = NormalWindow(menu_data)
        self.normal_window.show()

    def go_voice(self):
        self.close()
        self.voice_window = VoiceKiosk()
        self.voice_window.show()

    def go_recommend(self):
        from Recommend import RecommandOrder
        self.recommend = RecommandOrder(self.username)
        self.recommend.show()
        self.close()



class VoiceKiosk(QMainWindow):
    def backtoMain(self):
        self.close()
        self.mainwindow = MainWindow()
        self.mainwindow.show()

    def activate_microphone(self):
        if not self.listening:
            self.listening = True
            self.activate_button.setText("음성 입력 중지")
            self.label.setText("1초 후에 음성 입력을 시작합니다.")
            self.repaint()
            time.sleep(1)

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.label.setText("음성을 입력하세요...")
                self.repaint()
                audio_data = recognizer.listen(source)
                try:
                    user_input = recognizer.recognize_google(audio_data, language='ko-KR')
                    if self.check_menu(user_input):
                        self.update_order_display()
                        QMessageBox.information(self, "주문 추가", f"{user_input}을(를) 주문에 추가하였습니다.")
                        self.checkout_button.setEnabled(True)
                    else:
                        QMessageBox.warning(self, "주문 실패", "죄송합니다. 해당 메뉴가 없습니다.")
                except sr.UnknownValueError:
                    QMessageBox.warning(self, "음성 인식 실패", "음성을 인식할 수 없습니다.")
            self.listening = False
            self.activate_button.setText("음성 입력 시작")
            self.label.setText("키오스크가 주문할 메뉴를 말씀해주세요.")

    def speak_instruction(self, instruction):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        engine.say(instruction)
        engine.runAndWait()

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(200, self.activate_voice_guide)

    def activate_voice_guide(self):

        self.speak_instruction("키오스크가 주문할 메뉴를 말씀해주세요.")

    def __init__(self):
        super().__init__()
        self.listening = False

        self.setWindowTitle("음성 주문 키오스크")
        self.setGeometry(100, 100, 480, 800)
        self.order_list = []

        layout = QVBoxLayout()

        self.label = QLabel("키오스크가 주문할 메뉴를 말씀해주세요.", self)
        self.label.setFont(QFont("Arial", 14))
        layout.addWidget(self.label)

        self.activate_button = QPushButton("음성 입력 시작", self)
        self.activate_button.clicked.connect(self.activate_microphone)
        layout.addWidget(self.activate_button)

        self.order_label = QLabel("주문 목록:", self)
        self.order_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.order_label)

        self.order_display = QVBoxLayout()
        layout.addLayout(self.order_display)

        self.checkout_button = QPushButton("결제하기", self)
        self.checkout_button.setEnabled(False)
        self.checkout_button.clicked.connect(self.open_payment_screen)
        layout.addWidget(self.checkout_button)

        self.back_button = QPushButton("", self)
        self.back_button.setIcon(QIcon("back_icon.png"))
        self.back_button.setIconSize(self.back_button.sizeHint())
        self.back_button.setMaximumSize(20, 50)
        layout.addWidget(self.back_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "1234"
        self.db_database = "kiosk"

        self.db_connection = None

        self.connect_to_database()
        self.back_button.clicked.connect(self.backtoMain)

    def check_menu(self, user_input):
        if self.db_connection is None:
            QMessageBox.warning(self, "연결 실패", "데이터베이스에 연결되어 있지 않습니다.")
            return False

        try:
            with self.db_connection.cursor() as cursor:
                sql = "SELECT * FROM menu WHERE name = %s"
                cursor.execute(sql, (user_input,))
                result = cursor.fetchone()
                if result:
                    menu_name = result[1]
                    menu_price = result[2]
                    self.order_list.append((menu_name, menu_price, 1))
                    print(f"{menu_name} - 가격: {menu_price}원")
                    return True
                else:
                    return False
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "쿼리 실패", f"쿼리 실행 중 오류 발생: {str(e)}")
            return False

    def update_order_display(self):

        for i in reversed(range(self.order_display.count())):
            widget = self.order_display.itemAt(i).widget()
            if widget is not None:
                self.order_display.removeWidget(widget)
                widget.deleteLater()

        for item in self.order_list:
            menu_name, menu_price, quantity = item
            total_price = menu_price * quantity
            menu_widget = QWidget()
            menu_layout = QHBoxLayout()

            menu_label = QLabel(f"{menu_name} , 총 가격: {total_price}원", self)
            menu_layout.addWidget(menu_label)

            minus_button = QPushButton("-", self)
            minus_button.clicked.connect(lambda _, q=quantity, i=item: self.adjust_quantity(i, q - 1))
            menu_layout.addWidget(minus_button)

            quantity_label = QLabel(str(quantity), self)
            menu_layout.addWidget(quantity_label)

            plus_button = QPushButton("+", self)
            plus_button.clicked.connect(lambda _, q=quantity, i=item: self.adjust_quantity(i, q + 1))
            menu_layout.addWidget(plus_button)
            menu_widget.setLayout(menu_layout)
            self.order_display.addWidget(menu_widget)

    def adjust_quantity(self, item, new_quantity):
        index = self.order_list.index(item)
        if new_quantity > 0:
            self.order_list[index] = (item[0], item[1], new_quantity)
            self.update_order_display()
        else:
            del self.order_list[index]
            self.update_order_display()

    def open_payment_screen(self):
        import Voice_Payment
        payment_screen = Voice_Payment.PaymentScreen()
        payment_screen.exec_()

    def connect_to_database(self):
        try:
            self.db_connection = mysql.connector.connect(host=self.db_host, user=self.db_user,
                                                         password=self.db_password, database=self.db_database)
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "연결 실패", f"데이터베이스 연결 중 오류 발생: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    username = "user"  # 사용자명을 직접 입력하거나 적절히 설정합니다.
    window = MainWindow(username)
    window.show()
    sys.exit(app.exec_())  # 이벤트 루프 시작

        self.setup_socket()

    def initUI(self):
        self.order_number_label = QLabel(f"주문 번호: {self.order_number}", self)
        self.order_number_label.setStyleSheet("font-size: 20pt;")

        self.menu_label = QLabel("메뉴 : ", self)
        self.menu_label.setStyleSheet("font-size: 20pt;")

        self.counter_payment_label = QLabel("결제 방식: 카운터에서 결제", self)
        self.counter_payment_label.setStyleSheet("font-size: 20pt;")

        self.counter_payment_button = QPushButton("카운터에서 결제", self)
        self.counter_payment_button.setStyleSheet("font-size: 16pt;")
        self.counter_payment_button.clicked.connect(self.open_payment_screen)

        layout = QVBoxLayout()
        layout.addWidget(self.order_number_label)
        layout.addWidget(self.menu_label)
        layout.addWidget(self.counter_payment_label)
        layout.addWidget(self.counter_payment_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_payment_screen(self):
        from Voice_Payment import PaymentScreen
        self.payment_screen = PaymentScreen(order_number=self.order_number)  # 주문 번호를 인자로 전달하여 PaymentScreen 생성
        self.payment_screen.show()
        self.order_number += 1

    def setup_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 9999))  # 포트 번호를 일관성 있게 설정
        self.server_socket.listen(5)
        print("서버 대기 중...")

        self.client_socket, self.client_address = self.server_socket.accept()
        print(f"클라이언트 {self.client_address}가 연결되었습니다.")
        self.receive_order_info()

    def receive_order_info(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            print("주문 정보 수신:", data.decode())

    def close_socket(self):
        self.client_socket.close()
        self.server_socket.close()

    def closeEvent(self, event):
        self.close_socket()
        event.accept()


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("로그인")
        self.setGeometry(100, 100, 280, 80)

        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("아이디:", self)
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit(self)
        layout.addWidget(self.username_edit)

        self.password_label = QLabel("비밀번호:", self)
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        self.login_button = QPushButton("로그인", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.user_type_label = QLabel("사용자 유형:", self)
        layout.addWidget(self.user_type_label)

        self.user_type_admin = QRadioButton("관리자", self)
        self.user_type_kiosk = QRadioButton("키오스크", self)
        layout.addWidget(self.user_type_admin)
        layout.addWidget(self.user_type_kiosk)

        self.register_button = QPushButton("회원가입", self)
        self.register_button.clicked.connect(self.show_register_window)
        layout.addWidget(self.register_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.exec_()

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not self.user_type_admin.isChecked() and not self.user_type_kiosk.isChecked():
            QMessageBox.warning(self, "경고", "사용자 유형을 선택해주세요.")
            return

        if self.user_type_admin.isChecked():
            if login_user(username, password, "관리자"):
                self.open_admin_window(username)
        elif self.user_type_kiosk.isChecked():
            if login_user(username, password, "키오스크"):
                print("Login successful")
                self.open_kiosk_window(username)

    def open_admin_window(self,username):
        from adminwindow.Admin_Display import AdminDisplay
        self.username = username
        admin_window = AdminDisplay(username=self.username_edit.text())
        admin_window.show()
        self.close()

    def open_kiosk_window(self,username):
        from MainWindow import MainWindow
        self.username = username

        print("Opening kiosk window")
        self.close()
        self.kiosk_window = MainWindow()
        self.kiosk_window.show()



class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("회원가입")
        self.setupUi()

    def setupUi(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("아이디:", self)
        layout.addWidget(self.username_label)
        self.username_edit = QLineEdit(self)
        layout.addWidget(self.username_edit)

        self.check_button = QPushButton("중복 확인", self)
        self.check_button.clicked.connect(self.check_duplicate)
        layout.addWidget(self.check_button)

        self.password_label = QLabel("비밀번호:", self)
        layout.addWidget(self.password_label)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        self.confirm_password_label = QLabel("비밀번호 확인:", self)
        layout.addWidget(self.confirm_password_label)
        self.confirm_password_edit = QLineEdit(self)
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_edit)

        self.register_button = QPushButton("회원가입", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def check_duplicate(self):
        username = self.username_edit.text()
        if not re.match("^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{4,}$", username):
            QMessageBox.warning(self, "유효성 검사", "아이디는 영문자와 숫자의 조합으로 최소 4자 이상이어야 합니다.")
            return

        try:
            # MySQL 데이터베이스 연결
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="kiosk"
            )

            # 커서 생성
            cursor = connection.cursor()

            # 사용자 정보 조회 쿼리
            select_query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(select_query, (username,))
            user = cursor.fetchone()

            if user:
                QMessageBox.warning(self, "중복 확인", "이미 존재하는 아이디입니다.")
            else:
                QMessageBox.information(self, "중복 확인", "사용 가능한 아이디입니다.")

        except mysql.connector.Error as e:
            print("MySQL 오류:", e)

        finally:
            # 연결 종료
            if connection.is_connected():
                cursor.close()
                connection.close()

    def register(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if not self.validate_username(username) or not self.validate_password(password, confirm_password):
            return

        if register_user(username, password):
                self.close()

    def validate_username(self, username):
        if not re.match("^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]{4,}$", username):
            QMessageBox.warning(self, "유효성 검사", "아이디는 영문자와 숫자의 조합으로 최소 4자 이상이어야 합니다.")
            return False
        return True

    def validate_password(self, password, confirm_password):
        if password != confirm_password:
            QMessageBox.warning(self, "유효성 검사", "비밀번호와 비밀번호 확인이 일치하지 않습니다.")
            return False
        elif len(password) < 4:
            QMessageBox.warning(self, "유효성 검사", "비밀번호는 최소 4자 이상이어야 합니다.")
            return False
        return True

def register_user(username, password):
    try:
        # MySQL 데이터베이스 연결
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )

        # 커서 생성
        cursor = connection.cursor()

        # 사용자 정보 조회 쿼리
        select_query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(select_query, (username,))
        user = cursor.fetchone()

        if user:
            QMessageBox.warning(None, "회원가입 실패", "이미 존재하는 아이디입니다.")
            return False

        # 사용자 정보를 INSERT 쿼리로 테이블에 저장
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        user_data = (username, password)
        cursor.execute(insert_query, user_data)

        # 변경사항을 커밋
        connection.commit()

        QMessageBox.information(None, "회원가입 성공", "회원가입이 완료되었습니다.")
        return True

    except mysql.connector.Error as e:
        print("MySQL 오류:", e)
        return False

    finally:
        # 연결 종료
        if connection.is_connected():
            cursor.close()
            connection.close()

def login_user(username, password, user_type):
    try:
        # MySQL 데이터베이스 연결
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="kiosk"
        )

        # 커서 생성
        cursor = connection.cursor()

        # 사용자 정보 조회 쿼리
        select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        user_data = (username, password)
        cursor.execute(select_query, user_data)
        user = cursor.fetchone()

        if user:
            QMessageBox.information(None, "로그인 성공", f"{user_type} 로그인 성공")
            return True

        else:
            QMessageBox.warning(None, "로그인 실패", "아이디 또는 비밀번호가 일치하지 않습니다.")
            return False

    except mysql.connector.Error as e:
        print("MySQL 오류:", e)
        return False

    finally:
        # 연결 종료
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
