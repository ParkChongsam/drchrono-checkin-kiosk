from django import template
import datetime

register = template.Library()

@register.filter(name="msession")
def msession(value, arg):
    count = 0
    for a in value:
	t = a["appointment_start_time"]
	if t.hour in range(9,13) and arg == "1":
		count = count + 1
	elif t.hour in range(13,24) and arg == "0":
		count = count + 1 
    if count == 0:
	    return "none"
    return count


@register.filter(name="waitTime")
def waitTime(value, arg):
    minutes = 0
    apt = arg
    arv = value
    curr = datetime.datetime.now()
    diff = curr - max(arv,apt)
    datetime.timedelta(0, 8, 562000)
    m_s = divmod(diff.days * 86400 + diff.seconds, 60)
    return m_s[0]

@register.filter(name="duration")
def duration(value, arg):
    diff = arg - value
    datetime.timedelta(0, 8, 562000)
    m_s = divmod(diff.days * 86400 + diff.seconds, 60)
    return m_s[0]
     

