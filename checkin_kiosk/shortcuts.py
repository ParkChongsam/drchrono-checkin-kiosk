class Shortcuts(object):
	class Validations(object):
		INVALID_CREDENTIALS = 'No records found for entered first and last name combination'
	
	class Statuses(object):
		NOT_MENTIONED = 'Not Mentioned'
		NOT_CONFIRMED = 'Not Confirmed'
		ARRIVED = 'Arrived'
		CHECKED_IN = 'Checked In'
		IN_ROOM = 'In Room'
		CANCELLED = 'Cancelled'
		COMPLETE = 'Complete'
		CONFIRMED = 'Confirmed'
		IN_SESSION = 'In Session'
		NO_SHOW = 'No Show'
		RESCHEDULED = 'Rescheduled'
	
	class Gender(object):
		MALE = 'Male'
		FEMALE = 'Female'
		OTHER = 'Other'
	
	class Ethnicity(object):
		HISPANIC = 'hispanic'
		NOT_HISPANIC = 'not_hispanic'
		DECLINED = 'declined'
	
	class Race(object):
		INDIAN = 'indian'
		ASIAN = 'asian'
		HAWAIIAN = 'hawaiian'
		WHITE = 'white'
		BLACK = 'black'
		DECLINED = 'declined'
	
	class ErrorCodes(object):
		SUCCESS = 204