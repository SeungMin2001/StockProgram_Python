# ***StockProgram_Python***

- 키움증권 API, Dart API 를 사용한 자동매매 프로그램

- (Plan) : 5/1 ~ 6/1, Dart-Fss 를 이용한 자동매매 프로그램 완성시키기(Simulated Investment) <br>
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

### 받아올수 있는 정보들 



