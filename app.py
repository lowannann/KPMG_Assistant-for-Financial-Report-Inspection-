from flask import Flask, render_template
from flask import request as flask_request

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

# headless
from selenium.webdriver.chrome.options import Options  

import requests
import pandas as pd
from sympy import symbols

app=Flask(__name__)


@app.route("/")
def index():
    
    symbol=flask_request.args.get("symbol1")
    year=flask_request.args.get("year1")

    # symbol = '2603'
    # year = '107'

    # driverPath='/usr/local/bin/chromedriver'
    # browser=webdriver.Chrome(driverPath)
    # browser.implicitly_wait(30)
    
    # url0='https://mops.twse.com.tw/mops/web/t05st01'
    # browser.get(url0)

    # search_company=browser.find_element(By.XPATH,'/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[2]/table/tbody/tr/td[3]/div/div/input')
    # searching=search_company.send_keys("2603")
    # search_year=browser.find_element(By.XPATH,'/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[2]/table/tbody/tr/td[6]/div/div/input')
    # searching2=search_year.send_keys("107")
    # button = browser.find_element(By.XPATH,'/html/body/center/table/tbody/tr/td/div[4]/table/tbody/tr/td/div/table/tbody/tr/td[3]/div/div[3]/form/table/tbody/tr/td[4]/table/tbody/tr/td[2]/div/div/input')
    # button.click()

    print(symbol)

    if (symbol != None):
        url='https://mops.twse.com.tw/mops/web/ajax_t05st01'

        headers={'User=Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'}

        payload = {
            'encodeURIComponent': '1',
            'step': '1',
            'firstin': '1',
            'off': '1',
            'queryName': 'co_id',
            'inpuType': 'co_id',
            'TYPEK': 'all',
            'co_id': symbol,
            'year': year,
            }

    
        res=requests.post(url,headers=headers, data=payload)
        # print(res.text)
        df=pd.read_html(res.text)[1]
        contents=df[["主旨"]].values.tolist() #dataframe轉list
        speak_date=df["發言日期"].values.tolist()
        speak_time=df["發言時間"].values.tolist()

        print(speak_date) 

        list_info=[]
        list_line=[]


        for c in contents:
            for line in c:
                #jieba.load_userdict('for_jieba_dict.txt') #自訂義字典
                #cut=' '.join(jieba.cut(cc, cut_all=False, HMM=True))
                
                # print(line)
                list_line.append(line)

                
                
                if '公告本公司選任董事長' in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #0
                    
                elif '公告本公司取得' in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #1

                elif  '子公司' in line and '董事會決議' in line and '貨櫃' in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #2

                elif '新增背書保證金額' in line:
                    info='為他人背書保證/最近年度及截至年報刊印日止，股東會及董事會之重要決議' #3 #4

                elif '公告本公司購買' in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #7

                elif '本公司之子公司' in line and'購買'in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #8

                elif '本公司之子公司'in line and'取得'in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #9

                elif '本公司'in line and '異動' in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #10

                elif '代重要子公司'in line and '重要決議事項'in line: 
                    info='過去未被納入財報中' #11

                elif '代重要子公司'in line and '董事會決議'in line and '股東常會' in line:
                    info='過去未被納入財報中' #12

                elif '變動達三分之一以上'in line:
                    info='過去未被納入財報中' #13

                elif '董事會決議發放股利'in line:
                    info='過去未被納入財報中' #14

                elif '合併財務報告'in line:
                    info='過去未被納入財報中' #15

                elif '子公司'in line and '出售'in line and '貨櫃' in line:
                    info='過去未被納入財報中' #16

                elif '子公司'in line and '董事會決議'in line:
                    info='過去未被納入財報中' #17

                elif '累積處分'in line and '股票'in line:
                    info='過去未被納入財報中' #18

                elif '子公司'in line and '決議增資'in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議/label_20--採用權益法之投資' #19

                elif '公司債'in line:
                    info='公司債辦理情形' #21

                elif '澄清'in line and '報導'in line:
                    info='過去未被納入財報中' #23

                elif '更正'in line:
                    info='過去未被納入財報中' #24

                elif '有價證券於集中交易市場達公佈注意交易資訊標準'in line:
                    info='過去未被納入財報中' #25

                elif '公告本公司設置'in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議/label_27--公司治理運作情形及與上市上櫃公司治理實務守則差異情形及原因' #26

                elif '參加'in line and '法人說明會'in line:
                    info='公司治理運作情形及與上市上櫃公司治理實務守則差異情形及原因' #28

                elif '現金增資'in line:
                    info='資金運用計畫執行情形' #29

                elif '擬向'in line and '訂造'in line and '貨櫃'in line:
                    info='過去未被納入財報中' #30

                elif '電子投票'in line and '紀念品'in line:
                    info='過去未被納入財報中' #31

                elif '子公司'in line and '處分'in line and '貨櫃'in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #32

                elif '貨櫃船艘數調整'in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #33

                elif '公告本公司出售'in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #34

                elif '變更簽證會計師'in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #35

                elif '配息'in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #36

                elif '董事會決議' in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #6

                elif '說明'in line:
                    info='過去未被納入財報中' #22

                elif '股東常會' in line:
                    info='最近年度及截至年報刊印日止，股東會及董事會之重要決議' #5

                else:
                    info='過去未被納入財報中'
            
                list_info.append(info)
                # print(info)
                # results={
                #     '主旨':line,
                #     '分類':info
                # }

        # print(speak_date) 
        # print(speak_time)       
        # print(list_line) #主旨ok
        # print(list_info) #分類ok
        # print(results)
    
        return render_template("home.html",front_date=speak_date, front_time=speak_time, front_line=list_line,front_info=list_info)
    
    else:
        return render_template("home.html")


@app.route("/drive")
def drive():
    drive_id_back=flask_request.args.get("drive_id")
    
    if (drive_id_back != None):
        src_id="https://drive.google.com/file/d/"+drive_id_back+"/preview"
        return render_template("home.html",drive_id_front=src_id)
    else:
        return render_template("home.html")



# 如果你使用 python app.py 指令運行的話也能透過以下程式碼來啟動 flask 。
if __name__ == "__main__":
     app.run(debug=True, port=3000)
