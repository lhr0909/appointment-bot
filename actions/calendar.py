import os
import logging
from functools import lru_cache
from typing import Optional, List, Dict, Any, Text

import pendulum

from wechatpy.work.client import WeChatClient
from wechatpy.work.client.api import WeChatDepartment, WeChatUser, WeChatCalendar, WeChatSchedule

pendulum.set_locale('zh')

WECOM_CORP_ID = os.environ.get('WECOM_CORP_ID')
WECOM_CORP_SECRET = os.environ.get('WECOM_CORP_SECRET')

access_token = None

calendar_id = os.environ.get('WECOM_CALENDAR_ID')
calendar_user_id = os.environ.get('WECOM_CALENDAR_USER_ID')

logger = logging.getLogger(__name__)

client = WeChatClient(WECOM_CORP_ID, WECOM_CORP_SECRET, access_token=access_token)

@lru_cache(maxsize=10)
def get_all_calendar_schedules() -> List[Dict[Text, Any]]:
    result = []
    offset = 0
    limit = 1000
    schedules = client.schedule.get_by_calendar(calendar_id, offset, limit)
    while len(schedules) > 0:
        result = result + schedules
        offset = offset + limit
        schedules = client.schedule.get_by_calendar(calendar_id, offset, limit)
    return result

def get_schedules_that_overlaps(period: pendulum.Period):
    all_schedules = get_all_calendar_schedules()

    result = []

    for schedule in all_schedules:
        start_time = schedule.get("start_time")
        end_time = schedule.get("end_time")
        schedule_period = pendulum.period(pendulum.from_timestamp(start_time), pendulum.from_timestamp(end_time))
        if is_overlap(schedule_period, period):
            result.append(schedule)

    return result

def get_available_time_slots(time_from, time_to, duration_hour):
    get_all_calendar_schedules.cache_clear()

    period = pendulum.period(pendulum.parse(time_from), pendulum.parse(time_to))
    result = []

    for start in period.range('hours'):
        end = start.add(hours=duration_hour)
        time_slot_period = pendulum.period(start, end)
        overlapped_schedules = get_schedules_that_overlaps(time_slot_period)
        if len(overlapped_schedules) == 0:
            result.append(start.format('LLL'))

    return result

def get_available_time_slots_for_day(start_time, duration_hour):
    get_all_calendar_schedules.cache_clear()

    dt = pendulum.parse(start_time)
    # start time is 11am
    time_from = dt.add(hours=11-dt.hour)
    # end time is 7pm
    time_to = dt.add(hours=19-dt.hour)

    period = pendulum.period(time_from, time_to)
    result = []

    for start in period.range('hours'):
        end = start.add(hours=duration_hour)
        time_slot_period = pendulum.period(start, end)
        overlapped_schedules = get_schedules_that_overlaps(time_slot_period)
        if len(overlapped_schedules) == 0:
            result.append(start.format('LLL'))

    return result

def book_appointment(appointment_time_slot, duration_hour, appointment_item):
    start_time = pendulum.parse(appointment_time_slot)
    end_time = start_time.add(hours=duration_hour)

    period = pendulum.period(start_time, end_time)
    overlapped_schedules = get_schedules_that_overlaps(period)
    if len(overlapped_schedules) == 0:
        response = client.schedule.add(calendar_user_id, int(start_time.timestamp()), int(end_time.timestamp()), summary=appointment_item, calendar_id=calendar_id)
        logger.debug(response)
        return convert_datetime_string(appointment_time_slot)
    else:
        return None


def convert_datetime_string(time):
    return pendulum.parse(time).format('LLL')

def is_overlap(period_a, period_b):
    return get_overlap(period_a, period_b) is not None

def get_overlap(period_a: pendulum.Period, period_b: pendulum.Period) -> Optional[pendulum.Period]:
    """Returns the overlap between two periods."""
    start = max(period_a.start, period_b.start)
    end = min(period_a.end, period_b.end)
    # instant_overlap = period_a.start == period_b.start or start <= end
    # if instant_overlap or (start < end):
    if start < end:
        return pendulum.period(start, end)

if __name__ == '__main__':
    response = client.fetch_access_token()
    print(response['access_token'])
    # print(client.department.get())
    # print(client.user.list(1))
    # print(client.calendar.add(calendar_user_id, "预约机器人测试日历", "#FF00FF", "测试用日历"))
    # print(client.schedule.get_by_calendar(calendar_id, offset=0, limit=1000))
