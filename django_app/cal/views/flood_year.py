import calendar
from datetime import MAXYEAR
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.utils import timezone
from django.utils.safestring import SafeText
from .common import into_valid_range, get_month_list,\
                    get_prev_month, get_next_month,\
                    make_week_header

__all__ = [
    'flood_this_year',
    'flood_year',
    'next_year',
    'prev_year',
]

MINYEAR = 2


def flood_this_year(request):
    today = timezone.now()
    today_lt = timezone.localtime(today)

    return redirect('cal:flood_year', today_lt.year )


def flood_year(request, year):
    year = int(year)
    year = max(min(year, MAXYEAR), MINYEAR)

    month_list = get_month_list( (year,8), 13 )
    first_month = month_list[0]
    rend_data = gen_months(request, first_month[0], first_month[1], 27)

    context = {
            'rend_data': rend_data,
        }

    return render(request, 'cal/flood_year.html', context)


def next_year(request, year, month):
    year, month = into_valid_range(int(year), int(month))
    next_ym = get_next_month((year, month))

    return HttpResponse(gen_months(request, next_ym[0], next_ym[1], 3))


def prev_year(request, year, month):
    year, month = into_valid_range(int(year), int(month))
    prev_ym = get_prev_month((year, month), count=3)

    return HttpResponse(gen_months(request, prev_ym[0], prev_ym[1], 3))


def gen_months(request, year, month, count):
    year, month = into_valid_range(year, month)

    today = timezone.now()
    today_lt = timezone.localtime(today)

    firstweekday = request.session.get('firstweekday', 6)
    cal = calendar.Calendar(firstweekday)
    weekheader = make_week_header(firstweekday)

    rend_data = SafeText()
    for i in range(count):
        if today_lt.year == year and today_lt.month == month:
            today = today_lt.day
        else:
            today = None

        monthdays = cal.monthdayscalendar(year, month)

        context = {
            'grid_class': 'col-md-4',
            'year': year,
            'month': month,
            'today': today,
            'weekheader': weekheader,
            'monthdays': monthdays,
            'need_clearfix': None,
            }
        if (i+1) % 3 == 0:
            context['need_clearfix'] = True

        rend_data += loader.render_to_string('cal/grid_month.html', context, request)

        next_ym = get_next_month( (year, month) )
        if next_ym is None:
            break;

        year, month = next_ym

    return rend_data

