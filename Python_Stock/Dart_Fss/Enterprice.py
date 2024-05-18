import dart_fss as dart
class Dart():
    def __init__(self):
        self.api_key = '2c62c26d0182d996a0bad19b99513c5db41cc4df'
        dart.set_api_key(api_key=self.api_key)
        self.api_key = dart.get_api_key()
        self.corp_code = dart.api.filings.get_corp_code()
        self.find_name()

    def find_name(self):
        for index in self.corp_code:
            if index['corp_name'] == '삼성전자':
                print(index['corp_code'])
                return True


if __name__=="__main__": #메인 실행파일 명시
    Dart()

        


        

