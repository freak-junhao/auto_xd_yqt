import requests
import json
import time
from datetime import datetime
import numpy as np


def login_func(session, username, password):
    DEFAULT_HEADER = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                      "like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.89",
        "X-Requested-With": "XMLHttpRequest"
    }

    LOGIN_URL = "https://xxcapp.xidian.edu.cn/uc/wap/login/check"

    result = session.post(
        url=LOGIN_URL, data={'username': username, 'password': password},
        headers=DEFAULT_HEADER
    )

    return result.json()


def upload_func(session, data, login):
    if login != 0:
        return "未登录成功"

    DEFAULT_HEADER = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://xxcapp.xidian.edu.cn",
        "Referer": "https://xxcapp.xidian.edu.cn/site/ncov/xisudailyup"
    }

    # yi qing tong
    # DEFAULT_HEADER["Referer"] = "https://xxcapp.xidian.edu.cn/ncov/wap/default"
    # "https://xxcapp.xidian.edu.cn/ncov/wap/default/save"
    UPLOAD_URL = "https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save"

    result = session.post(
        url=UPLOAD_URL, data=data,
        headers=DEFAULT_HEADER
    )
    return result.json()["m"]


def _upload(users):
    for name, name_id, passwd in users:
        # start session with cookies
        sess = requests.Session()
        upload_time = datetime.now()
        upload_time = upload_time.strftime("%Y-%m-%d %H:%M:%S")

        # login
        login_res = login_func(sess, name_id, passwd)
        print("\n{} {} login {}".format(upload_time, name, login_res["m"]))

        # upload data
        upload_res = upload_func(sess, data_upload, login_res["e"])
        print("{} {} upload {}".format(upload_time, name, upload_res))


def check_time(ckpt, time_set):
    ckpt = ckpt.strftime("%H:%M")
    for i in time_set:
        if ckpt == i:
            return True
    return False


def sleep_time(ckpt, time_set):
    ckpt = ckpt.strftime("%H:%M")
    ckpt_time = datetime.strptime(ckpt, "%H:%M")
    for tt in time_set:
        if ckpt <= tt:
            tt_time = datetime.strptime(tt, "%H:%M")
            distance = (tt_time - ckpt_time).seconds
            return distance

    time1 = datetime.strptime(time_set[0], "%H:%M")
    time2 = datetime.strptime('00:00', "%H:%M")
    next_day = (time1 - time2).seconds

    time3 = datetime.strptime('00:00', "%H:%M")
    last_day = (time3 - ckpt_time).seconds
    distance = next_day + last_day
    return distance


if __name__ == '__main__':
    # time setting
    set_time = ['09:00', '14:00', '19:00']

    # get user names
    names = 'name.txt'
    name_ids = np.loadtxt(names, dtype=str)

    # get data from json
    json_file = 'default.json'
    with open(json_file, 'r') as f:
        data_upload = json.load(f)

    while True:
        # set upload time
        cur_time = datetime.now()
        dis = sleep_time(cur_time, set_time)
        if dis > 60:
            print('system sleeps in {}s'.format(dis - 60))
            time.sleep(dis - 60)
        else:
            if check_time(cur_time, set_time):
                _upload(name_ids)
                time.sleep(60 * 2)
