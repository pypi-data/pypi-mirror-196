


class Headers:
	def __init__(self):
		pass


	def official_api_headers(self, token: str, data = None):
		header = {
			"Authorization": f'Bearer {token}'
		}

		return header