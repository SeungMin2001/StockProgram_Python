from kiwoom.kiwoom import *  #키움클래스 가져오기
from PyQt5.QtWidgets import *
import sys
class Ui_class():
    def __init__(self):
        print("Ui")
        self.app = QApplication(sys.argv)

        self.kiwoom = Kiwoom()

        self.app.exec() #이벤트루프 실행

