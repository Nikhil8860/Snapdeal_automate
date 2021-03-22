import pymysql.cursors
import configparser


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
    query = """SELECT id FROM users WHERE invoice_number !='' AND exp_date  > NOW() """
    cursor.execute(query)
    info = cursor.fetchall()
    for i in info:
        db = "invento_" + str(i[0])
        conn = pymysql.connect(host=host, user=user, password=password, database=db)
        cursor_channel = conn.cursor()
        query_channel = """ SELECT id, user_id ,type FROM channels """
        cursor_channel.execute(query_channel)
        channel_info = cursor_channel.fetchall()
        conn.close()
        cursor_channel.close()
        yield channel_info


