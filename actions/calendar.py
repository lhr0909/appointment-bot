import os

import pendulum

from wechatpy.work.client import WeChatClient
from wechatpy.work.client.api import WeChatDepartment, WeChatUser, WeChatCalendar, WeChatSchedule

pendulum.set_locale('zh')

WECOM_CORP_ID = os.environ.get('WECOM_CORP_ID')
WECOM_CORP_SECRET = os.environ.get('WECOM_CORP_SECRET')

access_token = "wtksmvFP7joN3MQvo2mqIDxs_A9fpUhly0nX18MrcvTnxaCCqVK9uAd7x4yeHC1wOCNs7dnGOF57NCowWlxqRTI7J70fH6-zZi-c7S4l4wEgBzxn2cNOxUi1UNAh9HUMhObpvbIvW5qt7y1Xy4NAo0qtZP7YrMinEgyabm6B7-o4C9rhOdYbz-vsfIIBJ2V-GhhCAUhJw5tn6FOTyrRZmg"
# access_token = None

calendar_id = os.environ.get('WECOM_CALENDAR_ID')

client = WeChatClient(WECOM_CORP_ID, WECOM_CORP_SECRET, access_token=access_token)

def get_all_calendar_schedules():
    result = []
    offset = 0
    limit = 1000
    schedules = client.schedule.get_by_calendar(calendar_id, offset, limit)
    while len(schedules) > 0:
        result = result + schedules
        offset = offset + limit
        schedules = client.schedule.get_by_calendar(calendar_id, offset, limit)
    return result

def get_schedules_within_times(time_from, time_to):
    all_schedules = get_all_calendar_schedules()
    return list(filter(lambda x: x.get("start_time") >= time_from and x.get("end_time") <= time_to, all_schedules))

def get_available_schedules(time_from, time_to, duration_hour):
    dt_from = pendulum.parse(time_from)
    dt_to = pendulum.parse(time_to)
    period = pendulum.period(dt_from, dt_to)
    return list(map(lambda dt: dt.format('LLL'), period.range('hours')))

def convert_datetime_string(time):
    return pendulum.parse(time).format('LLL')

if __name__ == '__main__':
    response = client.fetch_access_token()
    print(response['access_token'])
    # print(client.department.get())
    # print(client.user.list(1))
    # print(client.calendar.add("simonl", "预约机器人测试日历", "#FF00FF", "测试用日历"))
    # print(client.schedule.get_by_calendar(calendar_id, offset=0, limit=1000))
