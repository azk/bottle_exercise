import datetime
import calendar
import os

from bs4 import BeautifulSoup
from bottle import route,run,template

import transforms
from utils import _a,_prev_next_month

PORT = int(os.environ.get("PORT",5000))


_calendar = calendar.HTMLCalendar(6)
def render_calendar(year,month = None):

	_html = _calendar.formatmonth(year,month) if month\
	 else _calendar.formatyear(year)

	return _html

@route('/')
@route('/<year:int>/<month:int>')
def month_view(year = None, month = None):

	if not (year or month):
		now = datetime.datetime.now()
		year = now.year
		month = now.month

	tbl = render_calendar(year,month)

	soup = BeautifulSoup(tbl)
	soup = transforms.format_table(soup)
	soup = transforms.add_weather(soup,year,month,True)
	
	prev_next = _prev_next_month(year,month)

	return template("main",cal_table=str(soup),
		prev=prev_next[0],next=prev_next[1],
		year=_a(year),_type="month")

@route('/<year:int>')
def year_view(year):
	
	tbl = render_calendar(year)
	soup = BeautifulSoup(tbl)
	soup = transforms.format_table(soup)
	soup = transforms.add_month_links(soup,year)

	return template("main",cal_table=str(soup),
		prev=_a(year-1),next=_a(year+1),_type="year")

if __name__ == "__main__":
	run(host="127.0.0.1",port = PORT,debug=True,reload=True)