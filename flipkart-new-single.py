import requests
from bs4 import BeautifulSoup
from time import sleep
import get_user


def read_details():
    f = open("log_flipkart.txt", 'a')
    all_info = get_user.read_details()
    for i in all_info:
        val = [j for j in i if j[2] == 'flipkart']
        for k in val:
            url_first = "http://cron.evanik.com/cron/flipkartcron.php?UserId="+str(k[1])+""
            url_hit_first = requests.get(url_first)
            soup_1 = BeautifulSoup(url_hit_first.text, 'html.parser')
            print(soup_1.text)
            f.write("USER ID " + str(i[1]) + 'CHANNEL_ID' + str(i[0]))
            f.write("\n")
            sleep(60)


if __name__ == '__main__':
    read_details()

