import weather
import calendar

from utils import _a

def format_table(soup):

	tables = soup.find_all('table')

	for table_tag in tables:
		cls = table_tag['class']

		cls.append('table')
		if "month" in cls:
			cls.append('table-striped')
		elif "year" in cls:
			cls.append('table-hover')

	return soup

def add_weather(soup,year,month,header_averages = False):

	cells = soup.find_all('td')
	avgs = weather.get_monthly_averages(year,month)

	for cell_tag in cells:
		
		try:
			day = int(cell_tag.text)
		except ValueError:
			continue

		weather_d = weather.get_temps(year,month,day)

		if weather_d is not None:
			
			cell_tag['data-toggle'] = "tooltip"


			cell_tag['title'] = "Min: {}\nMax: {}".format(
				weather_d[0],weather_d[1])		

			cls = cell_tag.get('class',[])

			cold = False
			if avgs[0] < weather_d[0]:
				cold = True
				cls.append("bg-info")

			if avgs[1] > weather_d[1]:
				if cold:
					cls.append("bg-warning")
				else:
					cls.append("bg-danger")

			cell_tag['class'] = cls

	if avgs and header_averages:
		headers = soup.find_all("th")

		for h in headers:
			cls = h.get('class')
			if cls and "month" in cls:

				h.string += " ({:,.2f} average min, {:,.2f} average max)".format(*avgs)

	return soup

_month_lookup = {m:i for i,m in enumerate(list(calendar.month_name))}
def add_month_links(soup,year):

	headers = soup.find_all("th")

	for header in headers:
		cls = header.get('class')

		if cls and 'month' in cls:
			month_num = _month_lookup[header.string]

			a = soup.new_tag("a")
			a['href'] = _a(year,month_num)

			header.string.wrap(a)

	return soup