import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
# import sched
# import time
headers_login = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",

}

def read_coo():
    try:
        with open("cookies.txt", "r") as fp:
            cookies = json.load(fp)
            if type(cookies)==type([]):
                cookies_dict = dict()
                for cookie in cookies:
                    cookies_dict[cookie['name']] = cookie['value']
                return cookies_dict
            else:
                return cookies
    except FileNotFoundError:

        return 0
def get_token(cookies_dict):
    url_login = "https://weixine.ustc.edu.cn/2020/home"

    r = requests.get(url_login,headers=headers_login,cookies=cookies_dict)
    r.raise_for_status()          #检验http状态码是否为200
    r.encoding = r.apparent_encoding#识别页面正确编码



    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    token=soup.find("input")
    if token == None:

        return token
    else:
        token=str(token).split('"')
        token=token[-2]
        coo = requests.utils.dict_from_cookiejar(r.cookies)
        with open("cookies.txt", "w") as fp:
            json.dump(coo, fp)

        return token
def daka(token,cookies_dict):
    data1={
    "_token":token,
    "now_address":"1",
    "gps_now_address":" ",
    "now_province":"340000",
    "gps_province":"",
    "now_city":"340100",
    "gps_city":"",
    "now_country":"340111",
    "gps_country":"",
    "is_inschool":'2',
    "body_condition":'1',
    "now_status":"1",
    "has_fever":'0',
    "last_touch_sars":'0',
    "is_goto_danger":"0",
    "is_danger":'0',
    'jinji_lxr':"温元香",
    "jinji_guanxi":"妈",
    "jiji_mobile":'13540608825',
    "other_detail":"",
    "confirm-report-hook":"1"
    }
    # print(data1)
    url_post = "https://weixine.ustc.edu.cn/2020/daliy_report"
    s=requests.session()

    r = s.post(url_post,headers=headers_login,cookies=cookies_dict,data=data1)

    r.raise_for_status()          #检验http状态码是否为200
    r.encoding = r.apparent_encoding#识别页面正确编码
    # print(r.cookies)

    html=r.text
    soup = BeautifulSoup(html, 'html.parser')
    staus= soup.find("p", class_='alert alert-success').text
    staus=str(staus)

    with open("历史打卡记录.txt",'a') as daka:

        daka.write(time1)
        if staus != []:
            daka.write(staus+"\n")
        else:
            daka.write("信息错误")
    # print(time1 + staus)
# def timedTask():
#     scheduler = sched.scheduler(time.time,time.sleep)
#     scheduler.enter(10,1,task)
#     scheduler.run()
# def task():
#     print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
def auto_login():
    import ustc_login
    ustc_login.auto_login()
    with open("历史打卡记录.txt", 'a') as daka:
        daka.write(time1)
        daka.write("启动自动化打卡" + "\n")
if __name__ == '__main__':
    time1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cookies_dict=read_coo()
    if cookies_dict==0:
        auto_login()
    else:
        token=get_token(cookies_dict)
        if token ==None:
            auto_login()
        else:
            with open("历史打卡记录.txt",'a') as f:
                f.write("\n")
            with open("历史打卡记录.txt", 'r') as f:
                data=f.read()
                now = datetime.now().strftime('%Y-%m-%d')
            if now in data:
                with open("历史打卡记录.txt", 'a') as daka:
                    daka.write(time1)
                    daka.write("已更新信息"+"\n")
            else:
                daka(token,cookies_dict)
