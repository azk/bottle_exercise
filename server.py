import datetime
import calendar
import os

from bs4 import BeautifulSoup
from bottle import route,run,template
import .weather

PORT = int(os.environ.get("PORT",5000))

class CalRenderer(object):
	
	def __init__(self,cal_object,tag_transform = None):
		self._calendar = cal_object
		self._tag_transform = tag_transform

	def render_calendar(self,year,month):

		_html = self._calendar.formatmonth(year,month) if month\
		 else self._calendar.formatyear(year)

		if self._tag_transform is not None:
			soup = BeautifulSoup(_html,"html.parser")

			for tag,transform in self._tag_transform.items():
				for t in soup.find_all(tag):
					transform(t,month,year)

			_html = str(soup)

		return _html

def _table_transform(table_tag,*args):

	cls = table_tag['class']

	cls.append('table')
	if "month" in cls:
		cls.append('table-striped')
	elif "year" in cls:
		cls.append('table-hover')

def _cell_transform(cell_tag,month,year):

	weather_d = weather.get_weather(cell_tag.text,month,year)

	if weather_d is not None:
		cell_tag['data-toggle'] = "tooltip" 
		cell_tag['title'] = "Popover title"

		cls = cell_tag.get('class',[])

		if "tue" in cls:
			cls.append("bg-info")

		cell_tag['class'] = cls

bs_transforms = {
	"table"	:	_table_transform,
	"td"	:	_cell_transform
}

CR = CalRenderer(calendar.HTMLCalendar(6),bs_transforms)

@route('/')
@route('/<year:int>')
@route('/<year:int>/<month:int>')
def display_calendar(year = None, month = None):

	if not (year or month):
		now = datetime.datetime.now()
		year = now.year
		month = now.month

	tbl = CR.render_calendar(year,month)

	return template("main",cal_table=tbl)

if __name__ == "__main__":
	run(host="0.0.0.0",port = PORT,debug=True,reload=True)