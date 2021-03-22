import requests

LOGIN_URL = "https://sellers.snapdeal.com/NewSnapdealLogin?refURL=http.sellers.snapdeal.com"
GET_URL = "https://sellers.snapdeal.com/sdSSOLogin?service=https%3A%2F%2Fseller.snapdeal.com%2F&targetUrl=%2F"


def login_snapdeal(user_name, password):
    payload = {"j_id0:navbar": "j_id0:navbar",
               "j_id0:navbar:txtUserName": user_name,
               "j_id0:navbar:txtPassword": password,
               "j_id0:navbar:j_id23": "j_id23: j_id0:navbar:j_id23",
               "com.salesforce.visualforce.ViewStateVersion": "202102101919080012"
               }

    with requests.Session() as s:
        s.headers['authority'] = "log.snapdeal.com"
        s.headers['accept-encoding'] = "gzip, deflate, br"
        s.headers[
            'User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        s.headers["Sec-Fetch-Site"] = "same-origin"
        s.headers["Sec-Fetch-Mode"] = "navigate"
        s.headers["Sec-Fetch-User"] = "?1"
        s.headers["Referer"] = "https://sellers.snapdeal.com/"
        s.headers["Origin"] = "https://sellers.snapdeal.com"
        s.headers["Host"] = "sellers.snapdeal.com"
        s.headers["Content-Type"] = "application/x-www-form-urlencoded"
        s.headers["Connection"] = "keep-alive"
        s.headers[
            "Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        r = s.post(LOGIN_URL, headers=s.headers, data=payload, verify=False)
        print(r.text)


if __name__ == '__main__':
    login_snapdeal('sgenterprises89@gmail.com', 'SD@@FEB@@19')
