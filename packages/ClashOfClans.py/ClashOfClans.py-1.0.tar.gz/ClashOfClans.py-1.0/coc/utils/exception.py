from json import loads

class UnknownError(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InvalidIp(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class NotFound(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class BadRequest(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


errors = {
	'accessDenied.invalidIp': InvalidIp,
	'notFound': NotFound,
	'badRequest': BadRequest
}


def checkException(data):
	try:
		data = loads(data)
		reason = data.get('reason')
	except:
		raise UnknownError(data)

	if reason in errors: raise errors.get(reason)(data)
	else:raise UnknownError(data)