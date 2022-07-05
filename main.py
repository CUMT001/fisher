# -*- coding: utf-8 -*-
import base64
import calendar
import datetime
from urllib import request
from webbrowser import get
import schedule
import time
import requests
import logging
import json
import base64

# import click
from zhdate import ZhDate as lunar_date
from business_calendar import Calendar, MO, TU, WE, TH, FR

from workday import getWorkDays


def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


def workday_parse():
    today = datetime.date.today()
    springFestival = lunar_date(today.year, 1, 1).to_datetime().date()
    nextSpringFestival = lunar_date(today.year + 1, 1, 1).to_datetime().date()
    distance_big_year = getWorkDays("{}-{}-{}".format(springFestival.year, springFestival.month, springFestival.day))
    distance_big_year = distance_big_year if distance_big_year > 0 else \
        250 + distance_big_year
    #     getWorkDays("{}-{}-{}".format(nextSpringFestival.year, nextSpringFestival.month, nextSpringFestival.day))

    duanwuFestival = lunar_date(today.year, 5, 5).to_datetime().date()
    nextDuanwuFestival = lunar_date(today.year + 1, 5, 5).to_datetime().date()
    distance_5_5 = getWorkDays("{}-{}-{}".format(duanwuFestival.year, duanwuFestival.month, duanwuFestival.day))
    distance_5_5 = distance_5_5 if distance_5_5 > 0 else \
        250 + distance_5_5
    #     getWorkDays("{}-{}-{}".format(nextDuanwuFestival.year, nextDuanwuFestival.month, nextDuanwuFestival.day))

    zhongqiuFestival = lunar_date(today.year, 8, 15).to_datetime().date()
    nextzhongqiuFestival = lunar_date(today.year + 1, 8, 15).to_datetime().date()
    distance_8_15 = getWorkDays("{}-{}-{}".format(zhongqiuFestival.year, zhongqiuFestival.month, zhongqiuFestival.day))
    distance_8_15 = distance_8_15 if distance_8_15 > 0 else \
        250 + distance_8_15
    #     getWorkDays("{}-{}-{}".format(nextzhongqiuFestival.year, nextzhongqiuFestival.month, nextzhongqiuFestival.day))

    initweekday, day = calendar.monthrange(today.year, today.month)
    lastweekday = day % 7 + initweekday - 1
    if (lastweekday == 5):
        day = day - 1
    elif (lastweekday == 6):
        day = day - 2
    distance_salary = getWorkDays("{}-{}-{}".format(today.year, today.month, day))

    distance_year = getWorkDays("{}-01-01".format(today.year))
    distance_year = distance_year if distance_year > 0 else \
        getWorkDays("{}-01-01".format(today.year + 1))

    distance_4_5 = getWorkDays("{}-04-05".format(today.year))
    distance_4_5 = distance_4_5 if distance_4_5 > 0 else \
        getWorkDays("{}-04-05".format(today.year + 1))

    distance_5_1 = getWorkDays("{}-05-01".format(today.year))
    distance_5_1 = distance_5_1 if distance_5_1 > 0 else \
        getWorkDays("{}-05-01".format(today.year + 1))

    distance_10_1 = getWorkDays("{}-10-01".format(today.year))
    distance_10_1 = distance_10_1 if distance_10_1 > 0 else \
        getWorkDays("{}-10-01".format(today.year + 1))

    time_ = [
        {"v_": 5 - 1 - today.weekday(), "title": "周末"},  # 距离周末
        {"v_": distance_salary, "title": "发工资"}, # 发工资
        {"v_": distance_year, "title": "元旦"},  # 距离元旦
        {"v_": distance_big_year, "title": "过年"},  # 距离过年
        {"v_": distance_4_5, "title": "清明节"},  # 距离清明
        {"v_": distance_5_1, "title": "劳动节"},  # 距离劳动
        {"v_": distance_5_5 - 1, "title": "端午节"},  # 距离端午
        {"v_": distance_8_15, "title": "中秋节"},  # 距离中秋
        {"v_": distance_10_1, "title": "国庆节"},  # 距离国庆
    ]
    time_ = sorted(time_, key=lambda x: x['v_'], reverse=False)
    return time_


def time_parse(today):
    distance_big_year = (lunar_date(today.year, 1, 1).to_datetime().date() - today).days
    distance_big_year = distance_big_year if distance_big_year > 0 else (
            lunar_date(today.year + 1, 1, 1).to_datetime().date() - today).days

    distance_5_5 = (lunar_date(today.year, 5, 5).to_datetime().date() - today).days
    distance_5_5 = distance_5_5 if distance_5_5 > 0 else (
            lunar_date(today.year + 1, 5, 5).to_datetime().date() - today).days

    distance_8_15 = (lunar_date(today.year, 8, 15).to_datetime().date() - today).days
    distance_8_15 = distance_8_15 if distance_8_15 > 0 else (
            lunar_date(today.year + 1, 8, 15).to_datetime().date() - today).days

    initweekday, day = calendar.monthrange(today.year, today.month)
    lastweekday = day % 7 + initweekday - 1
    if (lastweekday == 5):
        day = day - 1
    elif (lastweekday == 6):
        day = day - 2
    distance_salary = (datetime.datetime.strptime(f"{today.year}-{today.month}-{day}", "%Y-%m-%d").date() - today).days

    distance_year = (datetime.datetime.strptime(f"{today.year}-01-01", "%Y-%m-%d").date() - today).days
    distance_year = distance_year if distance_year > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-01-01", "%Y-%m-%d").date() - today).days

    distance_4_5 = (datetime.datetime.strptime(f"{today.year}-04-05", "%Y-%m-%d").date() - today).days
    distance_4_5 = distance_4_5 if distance_4_5 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-04-05", "%Y-%m-%d").date() - today).days

    distance_5_1 = (datetime.datetime.strptime(f"{today.year}-05-01", "%Y-%m-%d").date() - today).days
    distance_5_1 = distance_5_1 if distance_5_1 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-05-01", "%Y-%m-%d").date() - today).days

    distance_10_1 = (datetime.datetime.strptime(f"{today.year}-10-01", "%Y-%m-%d").date() - today).days
    distance_10_1 = distance_10_1 if distance_10_1 > 0 else (
            datetime.datetime.strptime(f"{today.year + 1}-10-01", "%Y-%m-%d").date() - today).days

    # print("距离大年: ", distance_big_year)
    # print("距离端午: ", distance_5_5)
    # print("距离中秋: ", distance_8_15)
    # print("距离元旦: ", distance_year)
    # print("距离清明: ", distance_4_5)
    # print("距离劳动: ", distance_5_1)
    # print("距离国庆: ", distance_10_1)
    # print("距离周末: ", 5 - today.weekday())

    time_ = [
        {"v_": 5 - 1 - today.weekday(), "title": "周末"},  # 距离周末
        {"v_": distance_salary, "title": "发工资"}, # 发工资
        {"v_": distance_year, "title": "元旦"},  # 距离元旦
        {"v_": distance_big_year, "title": "过年"},  # 距离过年
        {"v_": distance_4_5, "title": "清明节"},  # 距离清明
        {"v_": distance_5_1, "title": "劳动节"},  # 距离劳动
        {"v_": distance_5_5 - 1, "title": "端午节"},  # 距离端午
        {"v_": distance_8_15, "title": "中秋节"},  # 距离中秋
        {"v_": distance_10_1, "title": "国庆节"},  # 距离国庆
    ]

    time_ = sorted(time_, key=lambda x: x['v_'], reverse=False)
    return time_


def postMsg(fishStr: str):
    with open("./moyu.jpg", "rb") as fh:
        picBytes = fh.read()
        picCode = base64.b64encode(picBytes).decode('ascii')
    url = ""
    headers = {"Content-Type":"application/json"}
    datas = {
        "message":{
            "body":[
                 {
                     "content":fishStr,
                     "type":"TEXT"
                 } 
            ]
        }
    }
    datap = {
        "message":{
            "body":[
                 {
                     "content":picCode,
                     "type":"IMAGE"
                 }
            ]
        }
    }
    r = requests.post(url, json.dumps(datas))
    r = requests.post(url, json.dumps(datap))
    print(r.text)


# 周末不需要输出，节假日不需要输出.
def isNeedOut(date):
    with open("./holiday.json") as fh:
        holiday_data = json.load(fh)
        holiday_data = holiday_data['holiday']
        datestr = "{:0>2d}-{:0>2d}".format(date.month, date.day)
        for day in holiday_data.keys():
            if datestr == day and holiday_data[day]["holiday"]:
                return False
            
    return True


# @click.command()
def cli(time):
    """你好，摸鱼人，工作再累，一定不要忘记摸鱼哦 !"""
    from colorama import init, Fore
    init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
    print()
    today = datetime.date.today()
    if not isNeedOut(today):
        return
    now_ = f"{today.year}年{today.month}月{today.day}日"
    week_day_ = get_week_day(today)
    print(f'\t\t {Fore.GREEN}{now_} {week_day_}')
    str_ = "{} {}\n".format(now_, week_day_)
    if time:
        str_ += '''
{}月{}日，上午好，百度渔夫，工作再累，一定不要忘记摸鱼哦 !
有事没事起身去茶水间去廊道去天台走走，别老在工位上坐着。
多喝点水，钱是老板的，但命是自己的 !
'''.format(today.month, today.day)
    else:
        str_ += '''
{}月{}日，晚上好，百度渔夫，工作再累，一定不要忘记摸鱼哦 !
恭喜你又熬过一天，工资到手，抓紧时间关上电脑，迎接你的下班生活吧。
摸鱼法则，钱是老板的，但命是自己的 !
'''.format(today.month, today.day)
    print(f'{Fore.RED}{str_}')

    time_ = time_parse(today)
    time_2 = workday_parse()
    # for t_ in time_:
    #     print(f'\t\t {Fore.RED}距离{t_.get("title")}还有: {t_.get("v_")+1}天({t_.get("title")}个工作日)')
    for i in range(len(time_)):
        if time_[i]["v_"] >= time_2[i]["v_"]:
            if time_[i]["title"] == "周末":
                if time:
                    itemStr = '距离{}还有:{}天 ({}个工作日)'.format(time_[i]["title"], time_[i]["v_"] + 1, time_2[i]["v_"] + 1)
                else:
                    itemStr = '距离{}还有:{}天 ({}个工作日)'.format(time_[i]["title"], time_[i]["v_"], time_2[i]["v_"])
            else:
                if time:
                    itemStr = '距离{}还有:{}天 ({}个工作日)'.format(time_[i]["title"], time_[i]["v_"] + 1, time_2[i]["v_"] + 1)
                else:
                    itemStr = '距离{}还有:{}天 ({}个工作日)'.format(time_[i]["title"], time_[i]["v_"], time_2[i]["v_"])
            print(itemStr)
        else:
            if time:
                itemStr = '距离{}还有:{}天'.format(time_[i]["title"], time_[i]["v_"])
            else:
                itemStr = '距离{}还有:{}天'.format(time_[i]["title"]-1, time_[i]["v_"]-1)
            print(itemStr)
        str_ += itemStr + "\n"
    tips_ = "[友情提示] 三甲医院 ICU 躺一天平均费用大概一万块。\n你晚一天进 ICU，就等于为你的家庭多赚一万块。少上班，多摸鱼。\n"
    print(f'{Fore.RED}{tips_}')
    # print(tips_)
    str_ += tips_ + "\n"
    print(f'\t\t\t\t\t\t\t{Fore.YELLOW} 摸鱼办')
    str_ += "\t\t\t\t\t\t摸鱼办"
    print(str_)
    postMsg(str_)


if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET,
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # cli(True)
    firstTime = "10:30"
    lastTime = "19:30"
    schedule.every().monday.at(firstTime).do(cli, True)
    schedule.every().tuesday.at(firstTime).do(cli, True)
    schedule.every().wednesday.at(firstTime).do(cli, True)
    schedule.every().thursday.at(firstTime).do(cli, True)
    schedule.every().friday.at(firstTime).do(cli, True)
    schedule.every().monday.at(lastTime).do(cli, False)
    schedule.every().tuesday.at(lastTime).do(cli, False)
    schedule.every().wednesday.at(lastTime).do(cli, False)
    schedule.every().thursday.at(lastTime).do(cli, False)
    schedule.every().friday.at(lastTime).do(cli, False)
    # schedule.every().seconds.do(cli)
    while True:
        schedule.run_pending()
        time.sleep(3)
