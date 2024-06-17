import logging
import sys
import mysql.connector
from functools import partial
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

logging.basicConfig(filename='app.log', level=logging.DEBUG)

class RecommandOrder(QMainWindow):
    db_connection = None

    def __init__(self, username=None, menu_data=None, EatWhere=None, parent=None):
        super(RecommandOrder, self).__init__(parent)
        self.setWindowTitle('메뉴 추천')
        self.selected_details = []
        self.menu_data = menu_data
        self.EatWhere = EatWhere
        self.username = username
        self.selectedCategory = None
        self.category_buttons = []  # Initialize an empty list for category buttons

        self.setup_ui()
        self.db_connection = self.connect_to_db()

        if not self.db_connection:
            logging.error("데이터베이스 연결에 실패했습니다.")
        else:
            categories = self.fetch_categories_from_db()
            if categories:
                self.create_category_buttons(categories)
            else:
                logging.error("카테고리를 불러오는데 실패했습니다.")

    def setup_ui(self):
        self.setFixedSize(480, 830)
        self.BaseWidget = QWidget(self)
        self.BaseWidget.setGeometry(0, 0, 480, 830)
        self.BaseWidget.setStyleSheet("background-color:rgb(255,255,255);")
        self.setCentralWidget(self.BaseWidget)

        self.FontInfo = QFont("Cafe24 Ssurround Bold", 15)
        self.FontName = QFont("Cafe24 Ssurround Bold", 12)

        self.RCOrderStackWidget = QStackedWidget(self.BaseWidget)
        self.RCOrderStackWidget.setGeometry(QRect(0, 110, 480, 720))
        self.RCOrderStackWidget.setStyleSheet("background-color:rgb(255,255,255);")

        self.BtnGoHome = QPushButton(self.BaseWidget)
        self.BtnGoHome.setGeometry(10, 40, 60, 60)
        self.BtnGoHome.setText("홈")
        self.BtnGoHome.clicked.connect(self.back_logic)

        self.LblIntro = QLabel(self.BaseWidget)
        self.LblIntro.setGeometry(QRect(90, 40, 240, 60))
        self.LblIntro.setAlignment(Qt.AlignCenter)
        self.LblIntro.setText("메뉴 추천")
        self.LblIntro.setFont(self.FontInfo)

        self.LblRCResult = QLabel(self.BaseWidget)
        self.LblRCResult.setGeometry(QRect(90, 40, 240, 60))
        self.LblRCResult.setAlignment(Qt.AlignCenter)
        self.LblRCResult.setFont(self.FontInfo)
        self.LblRCResult.setHidden(True)

        self.BtnZoomin = self.make_zoom_btn("-", 340, 40, 60, 60)
        self.BtnZoomout = self.make_zoom_btn("+", 410, 40, 60, 60)

        self.setup_category_page()
        self.setup_detail_page()
        self.setup_result_page()

        self.RCOrderStackWidget.addWidget(self.PageRecommand)
        self.RCOrderStackWidget.addWidget(self.PageDetail)
        self.RCOrderStackWidget.addWidget(self.PageResult)
        self.RCOrderStackWidget.setCurrentWidget(self.PageRecommand)


    def make_zoom_btn(self, text, x, y, width, height):
        btn = QPushButton(text, self.BaseWidget)
        btn.setGeometry(QRect(x, y, width, height))
        btn.setStyleSheet(
            "border-radius: 30px; border: 2px solid rgba(0,0,0,0); background-color: rgba(0,176,246,150); color: rgba(0,0,0,150)")
        btn.setFont(self.FontInfo)

        if text == "-":
            btn.clicked.connect(self.zoom_in_clicked)
        elif text == "+":
            btn.clicked.connect(self.zoom_out_clicked)

        return btn

    def zoom_in_clicked(self):
        pass

    def zoom_out_clicked(self):
        pass

    def setup_category_page(self):
        self.PageRecommand = QWidget()
        self.PageRecommand.setGeometry(QRect(0, 0, 480, 500))
        self.RCOrderStackWidget.addWidget(self.PageRecommand)  # 이 코드가 필요합니다

    def setup_detail_page(self):
        self.PageDetail = QWidget()
        self.PageDetail.setGeometry(QRect(0, 0, 480, 700))  # Ensure correct geometry
        self.detailLayout = QVBoxLayout(self.PageDetail)
        self.detailTitle = QLabel("세부 사항 선택")
        self.detailTitle.setFont(self.FontInfo)
        self.detailLayout.addWidget(self.detailTitle)
        self.detailButtons = []  # Ensure this list is used to track detail buttons

        # Setup the button to proceed to the next page (Result Page)
        self.BtnGoToNextPage = QPushButton(self.PageDetail)
        self.BtnGoToNextPage.setGeometry(QRect(100, 540, 280, 60))
        self.BtnGoToNextPage.setText("선택하기")
        self.BtnGoToNextPage.setStyleSheet(
            "border-radius: 30px; border: 2px solid rgba(0,0,0,0); background-color: rgba(0,176,246,150); color: rgba(0,0,0,150)")
        self.BtnGoToNextPage.setFont(self.FontInfo)
        self.BtnGoToNextPage.clicked.connect(self.go_detail_page)
        self.detailLayout.addWidget(self.BtnGoToNextPage)

        # Initialize BtnCheckDetailResult here
        self.BtnCheckDetailResult = QPushButton("메뉴 확인 (0)", self.PageDetail)
        self.BtnCheckDetailResult.setFont(self.FontName)
        self.BtnCheckDetailResult.setStyleSheet(
            "border-radius: 21px; background-color: rgba(0,176,246,200); color: rgb(255,255,255);")
        self.BtnCheckDetailResult.clicked.connect(self.go_result_page)
        self.detailLayout.addWidget(self.BtnCheckDetailResult)

        self.RCOrderStackWidget.addWidget(self.PageDetail)  # Add PageDetail to stack widget

    def setup_result_page(self):
        self.PageResult = QWidget()
        self.PageResult.setGeometry(QRect(0, 0, 480, 700))
        self.resultLayout = QVBoxLayout(self.PageResult)
        self.resultLabel = QLabel("선택된 메뉴")
        self.resultLabel.setFont(self.FontInfo)
        self.resultLayout.addWidget(self.resultLabel)
        self.resultMenuLayout = QVBoxLayout()
        self.resultLayout.addLayout(self.resultMenuLayout)

    def create_category_buttons(self, categories):
        if not categories:
            return

        category_pages = QStackedWidget(self.PageRecommand)
        category_pages.setGeometry(15, 200, 450, 410)

        num_pages = (len(categories) + 3) // 4
        pages = []

        for i in range(num_pages):
            page = QWidget()
            layout = QGridLayout()
            layout.setSpacing(20)
            page.setLayout(layout)
            pages.append(page)
            category_pages.addWidget(page)

        navigation_layout = QHBoxLayout()
        btn_prev = QPushButton("이전")
        btn_next = QPushButton("다음")
        btn_prev.clicked.connect(lambda: self.navigate_pages(category_pages, -1))
        btn_next.clicked.connect(lambda: self.navigate_pages(category_pages, 1))

        navigation_layout.addWidget(btn_prev)
        navigation_layout.addWidget(btn_next)

        main_layout = QVBoxLayout()
        main_layout.addWidget(category_pages)
        main_layout.addLayout(navigation_layout)
        self.PageRecommand.setLayout(main_layout)

        for i, category in enumerate(categories):
            btn = self.make_category_btn(category)
            page_index = i // 4
            row = (i % 4) // 2
            col = (i % 4) % 2
            pages[page_index].layout().addWidget(btn, row, col, 1, 1)

            # Add selection button below the category buttons
            select_btn = QPushButton("선택")
            select_btn.setFont(self.FontName)
            select_btn.setStyleSheet(
                "border-radius: 21px; background-color: rgba(0,176,246,200); color: rgb(255,255,255);")
            select_btn.clicked.connect(partial(self.category_select_button_clicked, category))
            pages[page_index].layout().addWidget(select_btn, row + 1, col, 1, 1)  # Place below the category button

    def category_select_button_clicked(self, category):
        self.selectedCategory = category
        for btn in self.category_buttons:
            btn.setStyleSheet(
                "border: 1px solid rgba(0,0,0,0); border-radius: 21px; background-color: rgba(255,126,0,200); color: rgb(255,255,255);")
        self.BtnCheckDetailResult.setText("메뉴 확인 (0)")
        self.RCOrderStackWidget.setCurrentWidget(self.PageRecommand)

    def make_category_btn(self, text):
        btn = QPushButton(text)
        btn.setFont(self.FontName)
        btn.setFlat(True)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn.setStyleSheet(
            "border: 1px solid rgba(0,0,0,0); border-radius: 21px; background-color: rgba(255,126,0,200); color: rgb(255,255,255);")
        btn.clicked.connect(partial(self.category_btn_clicked, btn))
        self.category_buttons.append(btn)  # Append button to list for tracking
        return btn

    def category_btn_clicked(self, btn):
        try:
            self.selectedCategory = btn.text()
            self.load_detail_buttons()
            self.RCOrderStackWidget.setCurrentWidget(self.PageDetail)
        except Exception as e:
            logging.error(f"카테고리 버튼 클릭 중 오류 발생: {e}")
    def load_detail_buttons(self):
        try:
            for btn in self.detailButtons:
                btn.setParent(None)
            self.detailButtons = []

            if not self.selectedCategory:
                logging.warning("카테고리 선택 중 디테일 오류 발생.")
                return

            details = self.fetch_details_from_db(self.selectedCategory)

            if details:
                for detail in details:
                    btn = self.make_detail_btn(detail)
                    self.detailButtons.append(btn)
                    self.detailLayout.addWidget(btn)
            else:
                logging.warning(f"카테고리에서 디테일을 찾을 수 없음: {self.selectedCategory}")

        except Exception as e:
            logging.error(f"디테일 버튼을 로드 중 오류: {e}")

    def make_detail_btn(self, text):
        btn = QPushButton(text)
        btn.setFont(self.FontName)
        btn.setCheckable(True)
        btn.setStyleSheet(
            "border-radius: 21px; background-color: rgba(0,176,246,200); color: rgb(255,255,255);")
        btn.clicked.connect(self.detail_btn_clicked)
        return btn

    def detail_btn_clicked(self):
        selected_details = [btn.text() for btn in self.detailButtons if btn.isChecked()]
        self.selected_details = selected_details
        self.BtnCheckDetailResult.setText(f"메뉴 확인 ({len(selected_details)})")

    def go_detail_page(self):
        self.RCOrderStackWidget.setCurrentWidget(self.PageDetail)

    def go_result_page(self):
        self.display_selected_menu()
        self.RCOrderStackWidget.setCurrentWidget(self.PageResult)

    def display_selected_menu(self):
        self.resultMenuLayout.setAlignment(Qt.AlignTop)
        self.resultMenuLayout.setSpacing(5)

        # Clear existing widgets from the layout
        for i in reversed(range(self.resultMenuLayout.count())):
            widget = self.resultMenuLayout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Add selected menu items to the layout
        for menu in self.selected_details:
            lbl_menu = QLabel(menu)
            lbl_menu.setFont(self.FontName)
            lbl_menu.setStyleSheet("color: rgb(0, 0, 0);")
            self.resultMenuLayout.addWidget(lbl_menu)

    def connect_to_db(self):
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="1234",
                database="kiosk"
            )
            return db_connection
        except mysql.connector.Error as err:
            logging.error(f"Database connection error: {err}")
            return None
    def fetch_categories_from_db(self):
        categories = []
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT DISTINCT category FROM menu WHERE username = %s", (self.username,))
            categories = [item[0] for item in cursor.fetchall()]
        except mysql.connector.Error as err:
            logging.error(f"데이터베이스에 안맞는 카테고리 오류발생: {err}")
        finally:
            cursor.close()
            return categories

    def fetch_details_from_db(self, category):
        details = []
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT detail FROM details WHERE category = %s", (category,))
            details = [item[0] for item in cursor.fetchall()]
        except mysql.connector.Error as err:
            logging.error(f"데이터베이스에 안맞는 카테고리 오류발생: {err}")
        finally:
            cursor.close()
            return details

    def back_logic(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    main_window = RecommandOrder()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
