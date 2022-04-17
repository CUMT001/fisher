from business_calendar import Calendar, MO, TU, WE, TH, FR
import datetime
import json

def getWorkDays(hdate: str) -> int:
    restday = datetime.datetime.strptime(hdate, "%Y-%m-%d").date()
    today = datetime.date.today()
    td = datetime.datetime.combine(today, datetime.datetime.min.time())
    cal = Calendar()
    month = restday.month
    day = restday.day
    year = restday.year
    date = datetime.datetime(int(year), int(month), int(day))
    # print('%s days between %s and %s' % (cal.busdaycount(td, date), today, date))
    diff = cal.busdaycount(td, date)

    with open("./holiday.json") as fh:
        holiday_data = json.load(fh)
        holiday_data = holiday_data['holiday']
        for day in holiday_data.keys():
            datestr = holiday_data[day]["date"]
            # import pdb;pdb.set_trace();
            dateh = datetime.datetime.strptime(datestr, "%Y-%m-%d")
            if dateh > td and dateh < date:
                if holiday_data[day]["holiday"] and dateh.weekday() < 5:
                    diff -= 1
                    # print(diff)
                elif not holiday_data[day]["holiday"]:
                    diff += 1
                    # print(diff)
                # print(holiday_data[day])

    return diff