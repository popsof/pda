import calendar
from datetime import MAXYEAR
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.utils import timezone
from django.utils.safestring import SafeText
from .common import into_valid_range, get_prev_month, get_next_month, get_month_list

__all__ = [
    'flood_this_month',
    'flood_month',
    'next_month',
    'prev_month',
]

MINYEAR = 2


def flood_this_month(request):
    today = timezone.now()
    today_lt = timezone.localtime(today)

    return redirect('cal:flood_month', today_lt.year, today_lt.month)
    

def flood_month(request, year, month):
    year = int(year)
    month = int(month)

    year, month = into_valid_range(year, month)

    month_list = get_month_list((year, month))
    print(month_list)
    
    table_data = SafeText()
    for month in month_list:
        table_data += gen_month(request, month[0], month[1])

    context = {
            'table_data': table_data,
            }

    return render(request, 'cal/flood_month.html', context)

def prev_month(request, year, month):
    year = int(year)
    month = int(month)

    if year < MINYEAR or year > MAXYEAR:
        return
    if month < 1 or month > 12:
        return

    next_ym = get_prev_month((year, month))
#    print( next_ym )
    return HttpResponse(gen_month(request, next_ym[0], next_ym[1]))    

def next_month(request, year, month):
    year = int(year)
    month = int(month)

    if year < MINYEAR or year > MAXYEAR:
        return
    if month < 1 or month > 12:
        return

    next_ym = get_next_month((year, month))
    return HttpResponse(gen_month(request, next_ym[0], next_ym[1]))    

def gen_month(request, year, month):
    today = timezone.now()
    today_lt = timezone.localtime(today)

    if today_lt.year == year and today_lt.month == month:
        today_day = today_lt.day
    else:
        today_day = -1

    firstweekday = request.session.get('firstweekday', 6)
    cal = calendar.Calendar(firstweekday)
#    print( 'year:{} month:{}'.format(year, month) )
    monthdays = cal.monthdays2calendar(year, month)

    context = {
            'year': year,
            'month': month,
            'monthdays': monthdays,
            'today': today_day,
            }
    
    return loader.render_to_string('cal/gen_month.html', context, request)

