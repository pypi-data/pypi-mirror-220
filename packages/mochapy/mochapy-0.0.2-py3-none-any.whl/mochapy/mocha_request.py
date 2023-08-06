class Request:
	def __init__(self, environment):
		self.environment = environment

	def path(self):
		return self.environment.get("PATH_INFO")

	def method(self):
		return self.environment.get("REQUEST_METHOD")