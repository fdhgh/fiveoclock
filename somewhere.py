import datetime as dt
import pytz
import random

def get_utc_now():
	utc_now = pytz.utc.localize(dt.datetime.utcnow())
	# adapted from https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python

	return utc_now

def get_fiveoclock_place(utc_now,common_only=True):
	timezones=pytz.common_timezones
	candidates = []
	minutes = []

	for tz_name in timezones:
	    tz = pytz.timezone(tz_name)
	    loc_now = utc_now.astimezone(pytz.timezone(tz_name))
	    if loc_now.hour == 17 and tz_name not in ["GMT","UTC"]:
	        candidates.append(tz_name)
	        minutes.append(loc_now.minute)

	if len(candidates) == 0:
		best_minute = 0
		winner = "Margaritaville"
	else:
		best_minute = min(minutes)
		winners = []
		i = 0
		while i < len(candidates):
		    if minutes[i] == best_minute:
		        winners.append(candidates[i])
		    i+=1
		winner = random.choice(winners)
	return winner, best_minute

def strip_location(locationa):
	locationb = locationa.replace("_"," ")
	occurrences = locationb.count("/")
	preposition = "in "

	if occurrences == 2:
		s1 = locationb.find("/")
		state = locationb[s1+1:]
		s2 = state.find("/")
		city = state[s2+1:]
		state = state[:s2]
		locationc = city + ", " + state
	else:
		while occurrences>1:
			s = locationb.find("/")
			if s>=0:
				locationb = locationb[s+1:]
				occurrences = locationb.count("/")
			else: occurrences=0
		s = locationb.find("/")
		locationc = locationb[s+1:]
		country = locationb[:s]

	if locationc in ["Eastern","Central","Pacific","Mountain","Atlantic"]:
		s = locationb.find("/")
		country = locationb[:s]
		locationc = locationc + " " + country

	if locationc in ["Easter"]:
		locationc  = locationc + " Island"
		preposition = "on "

	if locationc in ["Canary"]:
		locationc  = "the " + locationc + " Islands"

	if locationc[:4] in ["Isle"]:
		preposition = "on the "

	if locationc[:3] in ["St "]:
		locationc = "St. " + locationc[3:]

	if locationb[:10] in ["Antarctica"]: # case for Antarctic research stations ["Casey","Casey","Davis","DumontDUrville","Macquarie","Mawson","McMurdo","Palmer","Rothera","Syowa","Troll","Vostok"]:
		preposition = "at the "
		if locationc in ["DumontDUrville"]:
			locationc = "Dumont d'Urville Research Station, Antarctica"
		elif locationc in ["Macquarie"]:
			locationc = "Macquarie Island Research Station, Antarctica"
		else:
			locationc = locationc + " Research Station, Antarctica"

	stringl = preposition + locationc

	return stringl

def create_fiveoclock_string(minutes):
	if minutes ==0:
		stringa = "It's 5 o'clock "
	elif minutes == 1:
		##print("It's",minutes,"minute past 5 in",location)
		stringa = "It's " + str(minutes) + " minute past 5 "
	elif minutes >1:
		stringa = "It's " + str(minutes) + " minutes past 5 "

	return stringa

def somewhere():

	utc_now = get_utc_now()
	location,minutes = get_fiveoclock_place(utc_now,common_only=True)
	location = strip_location(location)
	stringa = create_fiveoclock_string(minutes)
	stringb = "Pour something tall and strong!"
	stringm = str('{:02d}'.format(minutes))

	return stringa,stringb,stringm,location

def main():
	stringa,stringb,stringm,location = somewhere()
	print("5:" + stringm + "pm")
	print(stringa + location + ".")
	print(stringb)

if __name__ == "__main__":
	main()
