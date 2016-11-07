import json
import pytz
import calendar
from datetime import MINYEAR, MAXYEAR
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.http import require_POST
from ..forms import MemoForm
from .common import get_prev_year, get_next_year,\
                    get_prev_month, get_next_month,\
                    make_week_header

__all__ = [
    'timezone_set',
    'this_month',
    'this_year',
    'cal_month',
    'cal_year',
    'cal_main',
    'set_memo',
]


def timezone_set(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        request.session['firstweekday'] = int(request.POST['firstweekday'])
        return redirect('cal:cal_main')
    else:
        firstweekday = request.session.get('firstweekday', 6)

        weeks = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

        context = {
            'timezones': pytz.common_timezones,
            'weeks': weeks,
            'firstweekday': firstweekday,
        }
        return render(request, 'cal/timezone_set.html', context)


def this_month(request):
    today = timezone.now()
    today_lt = timezone.localtime(today)

    return redirect('cal:cal_month', today_lt.year, today_lt.month)


def this_year(request):
    today = timezone.now()
    today_lt = timezone.localtime(today)

    return redirect('cal:cal_year', today_lt.year )


@require_POST
def set_memo(request, year, month, day):
    form = MemoForm(request.POST)
    if form.is_valid():
        ret = {
            'result': 'ok',
            'memo': form.cleaned_data['memo'],
            }
    else:
        context = {
            'form': form,
            }

        rend_form = loader.render_to_string('cal/memo_form.html', context, request)
        ret = {
            'result': 'error',
            'form': rend_form,
            }

    return HttpResponse(json.dumps(ret), content_type='application/json')

def cal_month(request, year, month):
    year = int(year)
    month = int(month)

    print(year, month)

    year = max(min(year, MAXYEAR), MINYEAR)
    month = max(min(month, 12), 1)

    cur_year_month = (year, month)
    prev_month = get_prev_month(cur_year_month)
    next_month = get_next_month(cur_year_month)
    prev_year = get_prev_year(cur_year_month)
    next_year = get_next_year(cur_year_month)

    today = timezone.now()
    today_lt = timezone.localtime(today)

    if today_lt.year == year and today_lt.month == month:
        today_day = today_lt.day
    else:
        today_day = -1

    firstweekday = request.session.get('firstweekday', 6)
    cal = calendar.Calendar(firstweekday)
    monthdays = cal.monthdays2calendar(year, month)
    weekheader = make_week_header(firstweekday)

    form = MemoForm()

    context = {
        'cur_month': cur_year_month,
        'prev_month': prev_month,
        'next_month': next_month,
        'prev_year': prev_year,
        'next_year': next_year,
        'weekheader': weekheader,
        'monthdays': monthdays,
        'today': today_day,
        'form': form,
    }

    return render(request, 'cal/cal_month.html', context)


def cal_year(request, year):
    year = int(year)
    year = max(min(year, MAXYEAR), MINYEAR)

    prev_year = year - 1
    prev_year = max(prev_year, MINYEAR)
    if prev_year == year:
        prev_year = None

    next_year = year + 1
    next_year = min(next_year, MAXYEAR)
    if next_year == year:
        next_year = None

    today = timezone.now()
    today_lt = timezone.localtime(today)

    if today_lt.year == year:
        today_month_day = (today_lt.month, today_lt.day)
    else:
        today_month_day = None

    firstweekday = request.session.get('firstweekday', 6)
    cal = calendar.Calendar(firstweekday)
    yeardays = cal.yeardays2calendar(year, 12)
    weekheader = make_week_header(firstweekday)

    context = {
        'cur_year': year,
        'prev_year': prev_year,
        'next_year': next_year,
        'weekheader': weekheader,
        'yeardays': yeardays[0],
        'today': today_month_day,
    }

    return render(request, 'cal/cal_year.html', context)


def cal_main(request):
    today = timezone.now()
    today_lt = timezone.localtime(today)

    return redirect('cal:cal_month', today_lt.year, today_lt.month)

