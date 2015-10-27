def _a(year,month = None):
	s = "/{}".format(year)

	if month:
		s += "/{}".format(month)

	return s

def _prev_next_month(year,month):
	if month == 12:
		return (_a(year,month-1),_a(year+1,1))
	elif month == 1:
		return (_a(year-1,12),_a(year,month+1))
	else:
		return (_a(year,month-1),_a(year,month+1))