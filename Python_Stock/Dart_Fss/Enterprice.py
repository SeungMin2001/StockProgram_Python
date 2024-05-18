import dart_fss as dart
class Dart():
    def __init__(self):
        self.api_key = '2c62c26d0182d996a0bad19b99513c5db41cc4df'
        dart.set_api_key(api_key=self.api_key)
        self.api_key = dart.get_api_key()
        self.corp_code = dart.api.filings.get_corp_code()
        self.company_name ='삼성전자'
        self.company_code = None
        self.situation()

    def find_name(self):
        for index in self.corp_code:
            if index['corp_name'] == self.company_name:
                return index['corp_code']
            
    def print_corp_info(slef, info):
        print("회사 이름:", info['corp_name'])
        print("영문 회사 이름:", info['corp_name_eng'])
        print("주식 종목 이름:", info['stock_name'])
        print("주식 코드:", info['stock_code'])
        print("대표자 이름:", info['ceo_nm'])
        print("법인 분류:", info['corp_cls'])
        print("법인 등록 번호:", info['jurir_no'])
        print("사업자 등록 번호:", info['bizr_no'])
        print("주소:", info['adres'])
        print("홈페이지:", info['hm_url'])
        print("전화 번호:", info['phn_no'])
        print("팩스 번호:", info['fax_no'])
        print("산업 코드:", info['induty_code'])
        print("설립일:", info['est_dt'])
        print("회계 월:", info['acc_mt'])

    def situation(self):
        self.company_code = self.find_name()
        result = dart.api.filings.get_corp_info(self.company_code)
        if result['status'] == '000':
            self.print_corp_info(result)
        else:
            print("회사 정보를 가져오는 데 실패했습니다.")



if __name__=="__main__": 
    Dart()

        


        

