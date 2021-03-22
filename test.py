import pymysql.cursors


def connection():
    conn = pymysql.connect(host="13.233.239.105", user="root",
                           password='evanik@2019', database="evanik_erp_cronjobs")

    cursor = conn.cursor()
    query = """SELECT UserId,UserName,PASSWORD,channel_id,TYPE,sellerId,updatetime FROM inv_userlist WHERE TYPE IN ('snapdeal') AND exp_date  > NOW() 
                AND active ='1' ORDER BY priority DESC,UserId DESC"""
    cursor.execute(query)
    info = cursor.fetchall()
    cursor.close()
    conn.close()
    user_id = []
    username = []
    password = []
    channel_id = []
    seller_id = []
    for i in info:
        user_id.append(i[0])
        username.append(i[1])
        password.append(i[2])
        channel_id.append(i[3])
        seller_id.append(i[5])
    return user_id, username, password, channel_id, seller_id


if __name__ == '__main__':
    user_id, username, password, channel_id, seller_id = connection()
    print(username)
    print(password)
