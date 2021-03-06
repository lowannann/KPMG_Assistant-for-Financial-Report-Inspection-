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
        contents=df[["??????"]].values.tolist() #dataframe???list
        speak_date=df["????????????"].values.tolist()
        speak_time=df["????????????"].values.tolist()

        print(speak_date) 

        list_info=[]
        list_line=[]


        for c in contents:
            for line in c:
                #jieba.load_userdict('for_jieba_dict.txt') #???????????????
                #cut=' '.join(jieba.cut(cc, cut_all=False, HMM=True))
                
                # print(line)
                list_line.append(line)

                
                
                if '??????????????????????????????' in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #0
                    
                elif '?????????????????????' in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #1

                elif  '?????????' in line and '???????????????' in line and '??????' in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #2

                elif '????????????????????????' in line:
                    info='?????????????????????/??????????????????????????????????????????????????????????????????????????????' #3 #4

                elif '?????????????????????' in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #7

                elif '?????????????????????' in line and'??????'in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #8

                elif '?????????????????????'in line and'??????'in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #9

                elif '?????????'in line and '??????' in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #10

                elif '??????????????????'in line and '??????????????????'in line: 
                    info='???????????????????????????' #11

                elif '??????????????????'in line and '???????????????'in line and '????????????' in line:
                    info='???????????????????????????' #12

                elif '???????????????????????????'in line:
                    info='???????????????????????????' #13

                elif '???????????????????????????'in line:
                    info='???????????????????????????' #14

                elif '??????????????????'in line:
                    info='???????????????????????????' #15

                elif '?????????'in line and '??????'in line and '??????' in line:
                    info='???????????????????????????' #16

                elif '?????????'in line and '???????????????'in line:
                    info='???????????????????????????' #17

                elif '????????????'in line and '??????'in line:
                    info='???????????????????????????' #18

                elif '?????????'in line and '????????????'in line:
                    info='??????????????????????????????????????????????????????????????????????????????/label_20--????????????????????????' #19

                elif '?????????'in line:
                    info='?????????????????????' #21

                elif '??????'in line and '??????'in line:
                    info='???????????????????????????' #23

                elif '??????'in line:
                    info='???????????????????????????' #24

                elif '??????????????????????????????????????????????????????????????????'in line:
                    info='???????????????????????????' #25

                elif '?????????????????????'in line:
                    info='??????????????????????????????????????????????????????????????????????????????/label_27--???????????????????????????????????????????????????????????????????????????????????????' #26

                elif '??????'in line and '???????????????'in line:
                    info='???????????????????????????????????????????????????????????????????????????????????????' #28

                elif '????????????'in line:
                    info='??????????????????????????????' #29

                elif '??????'in line and '??????'in line and '??????'in line:
                    info='???????????????????????????' #30

                elif '????????????'in line and '?????????'in line:
                    info='???????????????????????????' #31

                elif '?????????'in line and '??????'in line and '??????'in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #32

                elif '?????????????????????'in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #33

                elif '?????????????????????'in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #34

                elif '?????????????????????'in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #35

                elif '??????'in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #36

                elif '???????????????' in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #6

                elif '??????'in line:
                    info='???????????????????????????' #22

                elif '????????????' in line:
                    info='??????????????????????????????????????????????????????????????????????????????' #5

                else:
                    info='???????????????????????????'
            
                list_info.append(info)
                # print(info)
                # results={
                #     '??????':line,
                #     '??????':info
                # }

        # print(speak_date) 
        # print(speak_time)       
        # print(list_line) #??????ok
        # print(list_info) #??????ok
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



# ??????????????? python app.py ?????????????????????????????????????????????????????? flask ???
if __name__ == "__main__":
     app.run(debug=True, port=3000)
