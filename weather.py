import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

JSON_PATH = Path(__file__).parent.joinpath('ims-results.json')

def load_weather_data(path=JSON_PATH):
	
	with JSON_PATH.open() as f:
		jsn = json.load(f)

	years_d = defaultdict(lambda :defaultdict(dict))
	for reading in jsn:
		dt = datetime.strptime(reading['time_obs'],"%Y-%m-%dT%H:%M:%S")

		years_d[dt.year][dt.month][dt.day] = (reading['tmp_air_min'],reading['tmp_air_max'])

	for year,months in years_d.items():
		for month,days in months.items():
			monthly_min = 0
			monthly_max = 0
			monthly_count = 0

			for temps in days.values():
				monthly_min += temps[0]
				monthly_max += temps[1]
				monthly_count += 1

			years_d[year][month]['averages'] = (float(monthly_min)/monthly_count,
				float(monthly_max)/monthly_count)

	return years_d

_weather_data = load_weather_data()

def get_temps(year,month = None,day = None):

	d = _weather_data[year]

	if d and month:
		d = d[month]

	if d and day:
		d = d.get(day)

	return d if d else None

def get_monthly_averages(year,month):

	d = _weather_data[year][month]

	return d['averages'] if d else None