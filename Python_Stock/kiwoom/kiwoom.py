from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.erorCode import *
from PyQt5.QtTest import *
class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("키움")s

        ########### eventloop 모음
        self.login_event_loop = None
        self.detail_account_info_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop()
        ###########################

        ########### 스크린번호 모음
        self.screen_my_info = "2000"
        self.screen_calculation_stock = "4000"
        ###########################

        ########### 변수모음
        self.account_num = None
        ###########################

        ########### 계좌관련변수
        self.use_money = 0
        self.use_money_percent = 0.5
        ###########################

        ###### 변수모음
        self.account_stock_dict = {}
        ###########################

        self.get_ocx_instance()
        self.event_slots()

        self.signal_login_commConnect()
        self.get_account_info()
        self.detail_account_info()
        self.detail_account_mystock()

        self.calculator_fnc() #종목분석용, 임시

    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1") #레지스트리 제어(API사용)

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")

        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def login_slot(self, errCode):
        print(errCode)
        print(errors(errCode))
        self.login_event_loop.exit()

    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(String)" , "ACCNO")
        self.account_num = account_list.split(';')[2]
        print("나의 보유 계좌번호 %s " % self.account_num)

    def detail_account_info(self):
        print("예수금을 요청하는 부분")
        self.dynamicCall("SetInputValue(String , String)", "계좌번호" , self.account_num)
        self.dynamicCall("SetInputValue(String , String)", "비밀번호" , "0000")
        self.dynamicCall("SetInputValue(String , String)", "비밀번호입력매체구분" , "00")
        self.dynamicCall("SetInputValue(String , String)", "조회구분" , "2")
        self.dynamicCall("CommRqData(String, String, int, String)", "예수금상세현황요청", "opw00001", "0",self.screen_my_info)
        self.detail_account_info_event_loop = QEventLoop()
        self.detail_account_info_event_loop.exec()

    def detail_account_mystock(self, sPrevNext="0"):
        print("계좌평가 잔고내역 요청")
        self.dynamicCall("SetInputValue(String , String)", "계좌번호", self.account_num)
        self.dynamicCall("SetInputValue(String , String)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(String , String)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(String , String)", "조회구분", "2")
        self.dynamicCall("CommRqData(String, String, int, String)", "계좌평가잔고내역요청", "opw00018", sPrevNext, self.screen_my_info)
        self.detail_account_info_event_loop.exec()


    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == "예수금상세현황요청":
            deposit = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "예수금")
            print("예수금 %s" %int(deposit))

            self.use_money = int(deposit) * self.use_money_percent
            self.use_money = self.use_money / 4

            ok_deposit = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "출금가능금액")
            print("출금가능금액 %s" % int(ok_deposit))

            self.detail_account_info_event_loop.exit()

        if sRQName == "계좌평가잔고내역요청":
            total_buy_money = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "총매입금액")
            print("총매입금액 %s" % int(total_buy_money))

            total_profit_loss_rate = self.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "총수익률(%)")

            print("총수익률(%%) %s" % float(total_profit_loss_rate) )

            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            cnt = 0
            for i in range(rows):
                code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목번호")
                code = code.strip()[1:]
                code_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
                stock_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "보유수량")
                buy_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입가")
                learn_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,"수익률(%)")
                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
                total_chegual_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입금액")
                possible_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매매가능수량")

                if code in self.account_stock_dict:
                    pass
                else:
                    self.account_stock_dict.update({code: {}})

                code_nm = code_nm.strip()
                stock_quantity = int(stock_quantity.strip())
                buy_price = int(buy_price.strip())
                learn_rate = float(learn_rate.strip())
                current_price = float(current_price.strip())
                total_chegual_price = int(total_chegual_price.strip())

                self.account_stock_dict[code].update({"종목명": code_nm})
                self.account_stock_dict[code].update({"보유수량": code_nm})
                self.account_stock_dict[code].update({"매입가": code_nm})
                self.account_stock_dict[code].update({"수익률(%)": code_nm})
                self.account_stock_dict[code].update({"현재가": code_nm})
                self.account_stock_dict[code].update({"매입금액": code_nm})
                self.account_stock_dict[code].update({"매매가능수량": code_nm})

                cnt += 1

            print("계좌에 가지고 있는 종목 %s" % self.account_stock_dict)
            print("계좌에 보유종목 카운트 %s" % cnt)

            if sPrevNext == "2":
                self.detail_account_mystock(sPrevNext="2")
            else:
                self.detail_account_info_event_loop.exit()



            self.detail_account_info_event_loop.exit()

        if sRQName == "주식일봉차트조회":
            code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
            code=code.strip()
            print("%s 일봉데이터 요청" %code)

            rows = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)
            print(rows)

            if sPrevNext == "2":
                self.day_kiwoom_db(code=code, sPrevNext=sPrevNext)
            else:
                self.calculator_event_loop.exit()


    def get_code_list_by_market(self, market_code):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market_code)
        code_list = code_list.split(";")[:-1]
        return code_list


    def calculator_fnc(self):
        code_list = self.get_code_list_by_market("10")
        print("코스닥 갯수%s" % len(code_list))

        for idx, code in enumerate(code_list):
            self.dynamicCall("DisconnectRealData(QString)", self.screen_calculation_stock)
            print("%s / %s : KOSDAQ Stock code : %s is updating..." % (idx+1, len(code_list), code))
            self.day_kiwoom_db(code=code)





    def day_kiwoom_db(self, code=None, date=None, sPrevNext="0"):
        QTest.qWait(3600)
        self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
        self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")
        if date != None:
            self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)

        self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식일봉차트조회", "opt10081", sPrevNext, self.screen_calculation_stock)

        self.calculator_event_loop.exec_()
