
import re
import html



def sanitize_input(input_data):
	return html.escape(input_data)


def validate_form(userData, sanitize = True):
	# sanitize input data
	clean_user_data = {}
	if sanitize:
		for k in userData:
			clean_user_data[k] = sanitize_input(userData[k])
	else:
		clean_user_data = userData

	# validate user data
	pattrens = [
		"[a-zA-Z]+[_.]+[a-zA-Z0-9]+", 
		"[a-zA-Z0-9_-]+[@](aol|gmail|yahoo|outlook)+(.com)+",
		"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
	]

	

	messages = [
	  "Invalid username should be like this abc_123 or abc. abc",
	  "This email address is not valid",
	  "The password length must be at least 8 uppercase, lowercase letters, numbers, symbols like @aA123#*"
	]

	result = {}

	for i, key in enumerate(clean_user_data):
		if not re.match(pattrens[i], clean_user_data[key]):
			result[key] = messages[i]

	if len(result) > 0:
		return {"error": result}
	else:
		return {"good": clean_user_data}



def custom_validate(data, pattrens, messages, sanitize = True):
	clean_user_data = {}
	if sanitize:
		# sanitize input data
		for k in data:
			clean_user_data[k] = sanitize_input(data[k])
	else:
		clean_user_data = data

	result = {}

	for i, key in enumerate(clean_user_data):
		if not re.match(pattrens[i], clean_user_data[key]):
			result[key] = messages[i]

	if len(result) > 0:
		return {"error": result}
	else:
		return {"good": clean_user_data}

