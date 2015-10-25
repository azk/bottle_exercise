import datetime
import calendar
import os

from bottle import route,run

PORT = int(os.environ.get("PORT",5000))

@route('/')
@route('/<year:int>')
@route('/<year:int>/<month:int>')
def display_calendar(year = None, month = None):

	cl = calendar.HTMLCalendar(calendar.SUNDAY)

	if not (year or month):
		now = datetime.datetime.now()
		year = now.year
		month = now.month

	return  cl.formatmonth(year,month) if month else cl.formatyear(year)

run(host="0.0.0.0",port = PORT)