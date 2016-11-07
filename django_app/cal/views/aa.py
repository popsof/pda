def make_week_header(firstweekday):
    day_name = []
    weekday = firstweekday
    for i in range(7):
        day_name.append((weekday, calendar.day_abbr[weekday]))
        weekday += 1
        if weekday > 6: weekday = 0

    return day_name

