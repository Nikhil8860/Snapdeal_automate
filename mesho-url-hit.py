import get_user
import datetime
import requests
from bs4 import BeautifulSoup
from time import sleep

CURRENT_MONTH = datetime.datetime.now().month
CURRENT_YEAR = datetime.datetime.now().year

DATE = str(CURRENT_YEAR) + "-" + str(CURRENT_MONTH) + '-01'


def get():
    all_info = get_user.read_details()
    for i in all_info:
        val = [j for j in i if j[2] == 'meesho']
        for k in val:
            url_first = "http://cron.evanik.com/cronjobs/Meesho/Payment/meeshoPayment.php?UserID="+str(k[1])+"&channel_id="+str(k[0])+""
            url_second = "http://cron.evanik.com/cronjobs/Meesho/Payment/meeshoPayment2.php?UserID="+str(k[1])+"&channel_id="+str(k[0])+""
            url_order = "http://cron.evanik.com/regular/meesho.php?UserID="+str(k[1])+"&channel_id="+str(k[0])+"&Status=Invoice&StartDate="+str(DATE)+""
            url_order_hit = requests.get(url_order)
            soup = BeautifulSoup(url_order_hit.text, 'html.parser')
            print(soup.text)
            sleep(60)


if __name__ == '__main__':
    get()
