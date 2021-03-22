import pymysql.cursors
import configparser
import datetime
import requests
import re
from bs4 import BeautifulSoup
from time import sleep

BASE_URL = "http://cron.evanik.com/cronjobs/Amazon/api/reports.php?UserID="
CURRENT_MONTH = datetime.datetime.now().month
CURRENT_YEAR = datetime.datetime.now().year

DATE = str(CURRENT_YEAR) + "-" + str(CURRENT_MONTH) + '-01'


def read_details():
    f = open("log_amazon.txt", 'a')
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = config.get('db', 'host')
    user = config.get('db', 'user')
    password = config.get('db', 'password')
    database = config.get('db', 'database')
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
    except ConnectionError:
        pass
    cursor = conn.cursor()
    query = """SELECT UserId,channel_id FROM
                    inv_userlist WHERE TYPE IN ('amazon') AND exp_date  > NOW() 
                    AND active ='1' ORDER BY priority DESC,UserId DESC"""
    cursor.execute(query)
    info = cursor.fetchall()
    for i in info:
        url_first = "http://cron.evanik.com/cronjobs/Amazon/api/reports.php?UserID=" + str(i[0]) + "&channel_id=" + str(
            i[1]) + "&Type=ALL_ORDERS&startDate=" + DATE + ""
        url_second = "http://cron.evanik.com/cronjobs/Amazon/api/reports.php?UserID=" + str(
            i[0]) + "&channel_id=" + str(i[1]) + ""
        print(url_first)
        print(url_second)
        for _ in range(2):
            url_hit_first = requests.get(url_first)
            sleep(2)
        soup_1 = BeautifulSoup(url_hit_first.text, 'html.parser')
        data = soup_1.find('pre')
        try:
            if data.text:
                status = re.findall("status\D+\d+", data.text)
                if status:
                    for _ in range(2):
                        url_hit_second = requests.get(url_second)
                        sleep(2)
                    soup_2 = BeautifulSoup(url_hit_second.text, 'html.parser')
                    print(soup_2.text)
                else:
                    f.write("USER ID:--> " + str(i[0]) + 'CHANNEL_ID:--> ' + str(i[1]))
                    f.write("\n")
            else:
                f.write("USER ID " + str(i[0]) + 'CHANNEL_ID' + str(i[1]))
                f.write("\n")
                sleep(180)
        except AttributeError:
            f.write("USER ID " + str(i[0]) + 'CHANNEL_ID' + str(i[1]))
            f.write("\n")
            sleep(180)


if __name__ == '__main__':
    read_details()

