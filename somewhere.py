import datetime as dt
import pytz
import random



def get_utc_now():
    utc_now = pytz.utc.localize(dt.datetime.utcnow())
    # adapted from https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python
    return utc_now

def hrs_to_5pm(utc_now):
    utc_h = utc_now.hour
    d=17-utc_h
    return d

def mins_past_5pm(now):
    m = now.minute
    return m

def possible_timezones(hrs_to_5pm,common_only=True):

    # adapted from https://stackoverflow.com/questions/46036998/pytz-timezone-from-utc-offset
    # pick one of the timezone collections
    timezones = pytz.common_timezones


    desired_delta = dt.timedelta(hours=hrs_to_5pm)
    #print ("desired delta",desired_delta)

    null_delta = dt.timedelta(0, 0)
    results = []

    for tz_name in timezones:
        tz = pytz.timezone(tz_name)
        non_dst_offset = getattr(tz, '_transition_info', [[null_delta]])[-1]
        if desired_delta == non_dst_offset[0]:
            results.append(tz_name)

    return results


def best_candidate(candidates,utc_now):
    minutes = []
    i=0
    best_i= 0
    rand_flag=0
    while i < len(candidates):
        c = candidates[i]
        pst_now = utc_now.astimezone(pytz.timezone(c))
        m = mins_past_5pm(pst_now)
        minutes.append(m)
        if m==minutes[best_i]:
            best_i=i
            rand_flag=1
        elif m<minutes[best_i]:
            best_i=i
        i+=1

    if rand_flag==1:
        best_i = random.randint(0,best_i)

    return candidates[best_i],minutes[best_i]

def strip_location(locationa):
    locationb = locationa.replace("_"," ")
    occurrences = locationb.count("/")

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

    if locationc in ["Eastern","Central","Pacific","Mountain","Atlantic"]:
        s = locationb.find("/")
        country = locationb[:s]
        locationc = locationc + " " + country

    if locationc in ["Easter"]:
        locationc  = locationc + " Island"

    if locationc in ["Canary"]:
        locationc  = "the " + locationc + " Islands"

    return locationc


def somewhere():

	utc_now = get_utc_now()
	candidates = possible_timezones(hrs_to_5pm(utc_now),common_only=True)
	location,minutes=best_candidate(candidates,utc_now)
	location = strip_location(location)

	if minutes ==0:
		stringa = "It's 5 o'clock in "
	elif minutes == 1:
		##print("It's",minutes,"minute past 5 in",location)
		stringa = "It's " + str(minutes) + " minute past 5 in "
	else:
		stringa = "It's " + str(minutes) + " minutes past 5 in "

	stringb = "Pour something tall and strong!"

	return stringa,stringb,str('{:02d}'.format(minutes)),location

def main():
    stringa,stringb,minutes,location = somewhere()
    print(stringa + location + ".")
    print(stringb)

if __name__ == "__main__":
    main()
