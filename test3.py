from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from bs4 import BeautifulSoup
import os
import pymysql.cursors

global d

conn = pymysql.connect(host="117.239.182.180", user="root",
                       password='evanik@2019', database="evanik_erp_cronjobs")


cursor = conn.cursor()
query = """SELECT UserId,UserName,PASSWORD,channel_id,TYPE,sellerId,updatetime FROM userlist WHERE TYPE IN ('snapdeal') AND exp_date  > NOW() 
            AND active ='1' ORDER BY priority DESC,UserId DESC"""
cursor.execute(query)
info = cursor.fetchall()

# print(info)

UserId = []
UserName = []
PASSWORD = []
channel_id = []
sellerId = []
for i in info:
    UserId.append(i[0])
    UserName.append(i[1])
    PASSWORD.append(i[2])
    channel_id.append(i[3])
    sellerId.append(i[5])
cursor.close()
conn.close()

print(UserId)
print(UserName)
print(PASSWORD)
print(channel_id)
print(sellerId)


def enable_download_in_headless_chrome(browser, download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


chrome_options = Options()
log = open('log.txt', 'a')

# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'C:\Users\nikhils3\Desktop\chromedriver')
driver.maximize_window()

for userid, username, password, channelid, sellerId in zip(UserId, UserName, PASSWORD, channel_id, sellerId):
    _dir = os.path.join(f"{os.getcwd()}\\{userid}\\{channelid}")
    print(_dir)

    enable_download_in_headless_chrome(driver, _dir)
    driver.get('https://sellers.snapdeal.com/NewSnapdealLogin')
    sleep(2)
    try:
        # driver.find_element_by_id('j_id0:navbar:txtUserName').send_keys(username)
        # driver.find_element_by_xpath('//*[(@id = "j_id0\:navbar\:txtUserName")]').send_keys(username)
        driver.find_element_by_css_selector('#j_id0\:navbar\:txtUserName').send_keys(username)

        sleep(2)
    except Exception as e:
        print("FAIL", e)
        log.write(str(userid) + " " + str(username) + "\n")
    try:
        driver.find_element_by_id('j_id0:navbar:txtPassword').send_keys(password)
        sleep(2)
    except Exception as e:
        print("wrong")
        log.write(str(userid) + " " + str(username) + "\n")
    try:
        driver.find_element_by_class_name('sf-button-secondary').click()
        sleep(3)
    except Exception as e:
        print("Password wrong")
        log.write(str(userid) + " " + str(username) + "\n")

    driver.get('https://seller.snapdeal.com/report/get?category=Orders&pageSize=5&start=0')
    sleep(3)
    info = driver.page_source
    soup = BeautifulSoup(info, 'html.parser')
    data = soup.find('pre')
    # print(data.contents)
    sleep(5)

    with open('info.txt', 'w') as f:
        sleep(2)
        try:
            f.write(str(data.get_text()))
        except Exception as e:
            print("Wrong Password")
            log.write(str(userid) + " " + str(username) + "\n")
    f1 = open('info.txt')
    sleep(3)

    try:
        d = json.load(f1)
    except:
        pass
    try:
        for info in d['reports']:
            try:
                url = 'https://seller.snapdeal.com/report/download/FullOrder/' + str(info['code'])
                sleep(5)
                driver.get(url)
                sleep(2)
            except Exception as e:
                log.write(str(userid) + " " + str(username) + "\n")
                print("Error: ", e)
    except:
        log.write(str(userid) + " " + str(username) + "\n")
        pass
    sleep(10)
