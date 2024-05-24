#메인 첫 화면
import importlib
import sys
import time

import mysql.connector
import pyttsx3
import speech_recognition as sr
from PyQt5.QtCore import QSize, Qt, QCoreApplication, QMetaObject, QRect, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QDialog, \
    QMessageBox, QSizePolicy
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from PyQt5.QtWidgets import QMainWindow, QPushButton
from Normal import NormalWindow, get_menu_data_from_database  # Normal.py 파일에서 NormalWindow 클래스 import

from Recommend import MenuWidget


# MainWindow.py 파일


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("MainWindow initialized")
        self.initUI()

    def initUI(self):
        print("Initializing UI")
        self.MainWindow = Ui_MainWindow()
        self.MainWindow.setupUi(self)
        print("UI initialized")
        self.show()
class Ui_MainWindow(object):
    def go_manager(self):
        from adminwindow.Admin_Main import AdminMainWindow
        self.manager_window = AdminMainWindow()
        self.manager_window.show()


    def go_active(self):
        self.active_window = QMainWindow()
        self.active_ui = Ui_OrderMethod()
        self.active_ui.setupUi(self.active_window)
        self.active_window.show()



    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(480, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(480, 800))
        MainWindow.setMaximumSize(QSize(480, 800))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.takeoutbutton = QPushButton(self.centralwidget)
        self.takeoutbutton.setObjectName(u"takeoutbutton")
        self.takeoutbutton.setGeometry(QRect(10, 290, 220, 440))
        self.takeoutbutton.clicked.connect(self.go_active)

        self.Welcomelabel = QLabel(self.centralwidget)
        self.Welcomelabel.setObjectName(u"Welcomelabel")
        self.Welcomelabel.setGeometry(QRect(110, 40, 221, 131))
        font = QFont()
        font.setFamily(u"Arial Black")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.Welcomelabel.setFont(font)
        self.Welcomelabel.setAlignment(Qt.AlignCenter)
        self.zoominbutton = QPushButton(self.centralwidget)
        self.zoominbutton.setObjectName(u"zoominbutton")
        self.zoominbutton.setGeometry(QRect(330, 50, 61, 61))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(40)
        self.zoominbutton.setFont(font1)
        self.zoominbutton_2 = QPushButton(self.centralwidget)
        self.zoominbutton_2.setObjectName(u"zoominbutton_2")
        self.zoominbutton_2.setGeometry(QRect(410, 50, 61, 61))
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.zoominbutton_2.sizePolicy().hasHeightForWidth())
        self.zoominbutton_2.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamily(u"Arial")
        font2.setPointSize(44)
        self.zoominbutton_2.setFont(font2)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(350, 10, 101, 31))
        font3 = QFont()
        font3.setFamily(u"Arial")
        font3.setPointSize(15)
        font3.setBold(True)
        font3.setWeight(75)
        self.label.setFont(font3)
        self.label.setAlignment(Qt.AlignCenter)
        self.toolButton = QPushButton(self.centralwidget)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(10, 10, 51, 51))
        self.Welcomelabel_2 = QLabel(self.centralwidget)
        self.Welcomelabel_2.setObjectName(u"Welcomelabel_2")
        self.Welcomelabel_2.setGeometry(QRect(40, 220, 411, 51))
        self.Welcomelabel_2.setFont(font)
        self.Welcomelabel_2.setAlignment(Qt.AlignCenter)
        self.eatherebutton = QPushButton(self.centralwidget)
        self.eatherebutton.setObjectName(u"eatherebutton")
        self.eatherebutton.setGeometry(QRect(250, 290, 220, 440))
        self.eatherebutton.clicked.connect(self.go_active)

        MainWindow.setCentralWidget(self.centralwidget)

        self.toolButton.clicked.connect(self.go_manager)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)


        self.zoominbutton.clicked.connect(self.increase_font_size)
        self.zoominbutton_2.clicked.connect(self.decrease_font_size)

        self.font_size = 15

    def increase_font_size(self):
        self.font_size += 2
        self.update_font()

    def decrease_font_size(self):
        self.font_size -= 2
        self.update_font()

    def update_font(self):
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(self.font_size)
        self.label.setFont(font)
        self.Welcomelabel.setFont(font)
        self.Welcomelabel_2.setFont(font)
        self.zoominbutton.setFont(font)
        self.zoominbutton_2.setFont(font)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"키오스크", None))
        self.takeoutbutton.setText(QCoreApplication.translate("MainWindow", u"포장 주문", None))
        self.Welcomelabel.setText(QCoreApplication.translate("MainWindow", u"초보도\n"
"쉽고 간편하게\n"
"주문하세요", None))
        self.zoominbutton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.zoominbutton_2.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"글씨 크기", None))
        self.toolButton.setText("")
        self.Welcomelabel_2.setText(QCoreApplication.translate("MainWindow", u"메뉴에서 선택 / 포장 주문 선택", None))
        self.eatherebutton.setText(QCoreApplication.translate("MainWindow", u"먹고가기", None))


class Ui_OrderMethod(object):



    def setupUi(self, OrderMethod):
        if not OrderMethod.objectName():
            OrderMethod.setObjectName(u"OrderMethod")
        OrderMethod.resize(480, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OrderMethod.sizePolicy().hasHeightForWidth())
        OrderMethod.setSizePolicy(sizePolicy)
        OrderMethod.setMinimumSize(QSize(480, 800))
        OrderMethod.setMaximumSize(QSize(480, 800))
        self.centralwidget = QWidget(OrderMethod)
        self.centralwidget.setObjectName(u"centralwidget")
        self.chobo = QPushButton(self.centralwidget)
        self.chobo.setObjectName(u"chobo")
        self.chobo.setGeometry(QRect(10, 150, 230, 400))
        self.voice = QPushButton(self.centralwidget)
        self.voice.setObjectName(u"voice")
        self.voice.setGeometry(QRect(240, 150, 230, 400))
        self.recommend = QPushButton(self.centralwidget)
        self.recommend.setObjectName(u"recommend")
        self.recommend.setGeometry(QRect(10, 560, 461, 230))
        self.info = QLabel(self.centralwidget)
        self.info.setObjectName(u"info")
        self.info.setGeometry(QRect(30, 50, 411, 51))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(35)
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setAlignment(Qt.AlignCenter)
        OrderMethod.setCentralWidget(self.centralwidget)

        self.retranslateUi(OrderMethod)

        QMetaObject.connectSlotsByName(OrderMethod)
        self.chobo.clicked.connect(self.go_normal)
        self.voice.clicked.connect(self.go_voice)
        self.recommend.clicked.connect(self.go_recommend)

    def go_normal(self):
        self.go_normal_order()

    def go_normal_order(self):

        menu_data = get_menu_data_from_database()
        self.normal_window = NormalWindow(menu_data)
        self.normal_window.show()

    def go_voice(self):

        self.voice_window = VoiceKiosk()
        self.voice_window.show()

    def go_recommend(self):
        pass

    def retranslateUi(self, OrderMethod):
        OrderMethod.setWindowTitle(QCoreApplication.translate("OrderMethod", u"주문 방법 선택", None))
        self.chobo.setText(QCoreApplication.translate("OrderMethod", u"일반 주문", None))
        self.voice.setText(QCoreApplication.translate("OrderMethod", u"음성 주문", None))
        self.recommend.setText(QCoreApplication.translate("OrderMethod", u"메뉴 추천", None))
        self.info.setText(QCoreApplication.translate("OrderMethod", u"주문 방법 선택", None))

class VoiceKiosk(QMainWindow):

    def show_order_method_dialog(self):
        self.dialog = QDialog(self)
        order_method_ui = Ui_OrderMethod()
        order_method_ui.setupUi(self.dialog)
        self.dialog.exec_()

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
        self.back_button.clicked.connect(self.show_order_method_dialog)

    def show_order_method_dialog(self):
        self.order_method_dialog = Ui_OrderMethod()
        self.order_method_dialog.exec_()

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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  # 이벤트 루프 시작