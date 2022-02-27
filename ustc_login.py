import json
import logging
from selenium import webdriver
import time
import datetime

def auto_login():
    with open("userinfo.txt", "r") as f:
        data = f.read()
        data= data.split('\n')
        zhanghao=str(data[2])
        password=str(data[3])

    #
    # logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
    #                     filename='new.log',
    #                     filemode='w',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    #                     #a是追加模式，默认如果不写的话，就是追加模式
    #                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    #                     #日志格式
    #                     )
    # #########
    # web_options = webdriver.EdgeOptions()
    # web_options.binary_location = str(data[0])
    #
    path = str(data[1])
    driver = webdriver.Edge(executable_path = path)

    driver.get('https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin')
    driver.find_element_by_name("username").send_keys(zhanghao)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_id("login").click()
    time.sleep(3)

    coo = driver.get_cookies()
    with open("cookies.txt", "w") as fp:
         json.dump(coo, fp)

    driver.find_element_by_id("report-submit-btn-a24").click()
    staus= driver.find_element_by_class_name("flash-message.mgb10.pd020").text

    driver.close()
    with open("历史打卡记录.txt",'a') as daka:
        time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        daka.write(time1)
        if staus != []:
            daka.write('自动化：'+staus)
        else:
            daka.write('信息错误')
if __name__ == '__main__':
    auto_login()
# def read_cookies():
#     # 设置cookies前必须访问一次百度的页面
#     driver.get("https://weixine.ustc.edu.cn/2020/home")
#
#     with open("cookies.txt", "r") as fp:
#         cookies = json.load(fp)
#         for cookie in cookies:            # cookie.pop('domain')  # 如果报domain无效的错误
#             driver.add_cookie(cookie)
#     driver.get("https://weixine.ustc.edu.cn/2020/home")
# read_cookies()




