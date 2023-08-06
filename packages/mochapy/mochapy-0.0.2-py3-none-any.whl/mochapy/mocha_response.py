class Response:
	def __init__(self, start_response, views_directory, static_directory):
		self.views_directory = views_directory
		self.static_directory = static_directory
		self.status = ""
		self.header = ""
		self.body = ""
		self.start_response = start_response

	def __bytes__(self):
		self.start_response(self.status, self.header)
		return bytes(self.body.encode())

	def send(self, data):
		self.body = data;

	def render(self, file):
		file_to_open = self.views_directory + file
		with open(file_to_open, 'r') as data:
			self.body = data.read()

	def render_static_file(self, file):
		file_to_open = self.static_directory + file
		with open(file_to_open, 'r') as data:
			self.body = data.read()