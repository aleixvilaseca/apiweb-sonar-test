# -*- coding: utf-8 -*-
import calendar
import datetime
import time
import dateutil.relativedelta

def get_current_year():
    return datetime.datetime.now().year

def get_current_month():
    return datetime.datetime.now().month

def get_last_month():
    month = get_current_month() - 1
    if month == 0:
        return 12
    else:
        return month

def get_year_last_month():
    month = get_current_month() - 1
    year = get_current_year()
    if month == 0:
        return year -1
    else:
        return year

def get_last_day_of_last_month(get_as_date_time = False, date_time_format='%Y-%m-%d %H:%M:%S'):
    month = get_current_month()
    year = get_current_year()

    if month == 1:
        month = 12
        year = year - 1
    else:
        month = month -1

    if get_as_date_time:
        return datetime.datetime.strptime(f"{year}-{str(month).zfill(2)}-{calendar.monthrange(year, month)[1]} 23:59:59", date_time_format)
    else:
        return f"{year}-{str(month).zfill(2)}-{calendar.monthrange(year, month)[1]}"

def get_first_day_of_last_month(get_as_date_time = False):
    month = get_current_month()
    year = get_current_year()

    if month == 1:
        month = 12
        year = year - 1
    else:
        month = month - 1

    if get_as_date_time:
        return datetime.datetime.strptime(f"{year}-{str(month).zfill(2)}-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    else:
        return f'{year}-{str(month).zfill(2)}-01'

def convert_custom_time_string_to_another(time_string, original_format, new_format):
    if time_string == '' or time_string is None:
        return ''
    struct = time.strptime(time_string, original_format)
    return(time.strftime(new_format, struct))

def get_timestamp(format='%Y%m%d_%H%M%S'):
    return datetime.datetime.now().strftime(format)

def substract_one_month_from_today(format='%Y%m%d_%H%M%S'):
    today = datetime.datetime.now()
    today = today.date()
    last_month = today - dateutil.relativedelta.relativedelta(months=1)
    last_month_first_date = last_month.replace(day=1)
    return last_month_first_date.strftime(format)

def substract_n_months_from_today(n_months=1, format='%Y%m%d_%H%M%S'):
    today = datetime.datetime.now()
    today = today.date()
    last_month = today - dateutil.relativedelta.relativedelta(months=n_months)
    last_month_first_date = last_month.replace(day=1)
    return last_month_first_date.strftime(format)

def substract_one_year_from_today(format='%Y%m%d_%H%M%S'):
    today = datetime.datetime.now()
    today = today.date()
    last_year = today - dateutil.relativedelta.relativedelta(years=1)
    last_year_first_date = last_year.replace(day=1)
    return last_year_first_date.strftime(format)

def get_today_date(format=None):
    now = datetime.datetime.now()
    if format is not None:
        now = datetime.datetime.strftime(now, format)

    return now

