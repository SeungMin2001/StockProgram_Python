# ***StockProgram_Python***

- 키움증권 API, Dart API 를 사용한 자동매매 프로그램

- (Plan) : 5/1 ~ ---, Dart-Fss 를 이용한 자동매매 프로그램 완성시키기(Simulated Investment) <br>
<br><br><br>


### 나의 정보를 요청하고 받아올 함수들 설정하기
```python
  def event_slots(self):
    self.OnEventConnect.connect(self.login_slot)
    self.OnReceiveTrData.connect(self.trdata_slot)
```
OnEventConnect 와 login_slot함수 연결<br>
OnReceiveTrData 와 trdata_slot함수 연결<br><br>
```python
    def detail_account_info(self):
        self.dynamicCall("SetInputValue(String , String)", "계좌번호" , self.account_num)
        self.dynamicCall("SetInputValue(String , String)", "비밀번호" , "0000")
        self.dynamicCall("SetInputValue(String , String)", "비밀번호입력매체구분" , "00")
        self.dynamicCall("SetInputValue(String , String)", "조회구분" , "2")
        self.dynamicCall("CommRqData(String, String, int, String)", "예수금상세현황요청", "opw00001", "0",self.screen_my_info)
```
- CommRqData로 정보요청->OnReceiveTrData에서 정보받기->연결된trdata_slot로 정보공유->trdata_slot에서 정보사용<br><br>

이런식으로 정보를 받으면서 나만의 알고리즘을 사용해 자동매매프로그램을 만들면된다.

### Dart Class
이 클래스는 기업의 공시,재무재표 등을 얻어올수 있는 클래스다.<br>
공시로 호재가 발표되면 보통 그 기업은 급등하므로 그 구간을 노리기 위해 이 클래스를 사용한다.<br><br><br>

```python
def situation(self):
        self.company_code = self.find_name()
        result = dart.api.filings.get_corp_info(self.company_code)
        if result['status'] == '000':
            self.print_corp_info(result)
        else:
            print("회사 정보를 가져오는 데 실패했습니다.")
```
find_name():회사이름을 넣어주면 종목번호를 알려준다.<br>
get_corp_info():종목번호를 넣어주면 회사정보를 알려준다.<br>
print_corp_info():회사 정보들을 보기좋게 출력해준다<br>
<br>
```
<삼성전자 예시>
회사 이름: 삼성전자(주)
영문 회사 이름: SAMSUNG ELECTRONICS CO,.LTD
주식 종목 이름: 삼성전자
주식 코드: 005930
대표자 이름: 한종희, 경계현
법인 분류: Y
법인 등록 번호: 1301110006246
사업자 등록 번호: 1248100998
주소: 경기도 수원시 영통구  삼성로 129 (매탄동)
홈페이지: www.samsung.com/sec
전화 번호: 02-2255-0114
팩스 번호: 031-200-7538
산업 코드: 264
설립일: 19690113
회계 월: 12
```



