import pymysql.cursors
import configparser
import datetime


CURRENT_MONTH = datetime.datetime.now().month
CURRENT_YEAR = datetime.datetime.now().year

DATE = str(CURRENT_YEAR) + "-" + str(CURRENT_MONTH) + '-01'


def read_details():
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
                    inv_userlist WHERE TYPE IN ('flipkart') AND exp_date  > NOW() 
                    AND active ='1' ORDER BY priority DESC,UserId DESC"""
    cursor.execute(query)
    info = cursor.fetchall()
    f = open("log_flipkart.txt", 'a')

    for i in info:
        url_first = "http://cron.evanik.com/cronjobs/Flipkart/Orders/flipkart_self.php?UserID="+str(i[0])+"&channel_id="+str(i[1])+""
        print(url_first)

        # url_hit_first = requests.get(url_first)
        # soup_1 = BeautifulSoup(url_hit_first.text, 'html.parser')
        # result = re.findall("Without\s+Login", soup_1.text)
        # if result:
        #     print("Success")
        # else:
        #     print("FAIL!!!")
        #     f.write("USER ID " + str(i[0]) + 'CHANNEL_ID' + str(i[1]))
        #     f.write("\n")
        # sleep(60)


if __name__ == '__main__':
    read_details()

