import calendar
from datetime import MAXYEAR

MINYEAR = 2


def into_valid_range(year, month):
    year = max(min(year, MAXYEAR), MINYEAR)
    month = max(min(month, 12), 1)

    return (year, month)

def get_prev_month(year_month, count=1):
    year = year_month[0] - count // 12
    month = year_month[1] - count % 12

    if month < 1:
        year -= 1
        month += 12

    if year < MINYEAR: return None
    return (year, month)


def get_prev_year(year_month):
    year = year_month[0] - 1
    month = year_month[1]
    if year < MINYEAR:
        return None

    return (year, month)


def get_next_month(year_month, count=1):
    year = year_month[0] + count // 12
    month = year_month[1] + count % 12

    if month > 12:
        year += 1
        month -= 12

    if year > MAXYEAR: return None
    return (year, month)


def get_next_year(year_month):
    year = year_month[0] + 1
    month = year_month[1]
    if year > MAXYEAR:
        return None

    return (year, month)


def get_month_list(cur_ym, count_each=5):
    """
    cur_ym: (cur_year, cur_month)
    return: list of (year, month)
    valid range 2/1 ~ MAXYEAR/12
    """
    year = cur_ym[0]
    month = cur_ym[1]
    year = max(min(year, MAXYEAR), MINYEAR)
    month = max(min(month, 12), 1)
    mid_ym = (year, month)

    count_before = (year - MINYEAR) * 12 + month - 1
    count_after = (MAXYEAR - year) * 12 + 12 - month

    if count_before < count_each:
        count_after = min(count_after, count_each * 2 - count_before)
    elif count_after < count_each:
        count_before = min(count_before, count_each * 2 - count_after)
    else:
        count_before = count_each
        count_after = count_each


    month_list = [mid_ym, ]
    cur_pos = mid_ym
    for i in range(count_before):
        cur_pos = get_prev_month(cur_pos)
        month_list.insert(0, cur_pos)

    cur_pos = mid_ym
    for i in range(count_after):
        cur_pos = get_next_month(cur_pos)
        month_list.append(cur_pos)

    return month_list


def make_week_header(firstweekday):
    day_name = []
    weekday = firstweekday
    for i in range(7):
        day_name.append((weekday, calendar.day_abbr[weekday]))
        weekday += 1
        if weekday > 6: weekday = 0

    return day_name


