from mocha_response import Response

class Scanner:
	def __init__(self, source):
		self.src = source
		self.src_length = len(source)
		self.curr_char = ''
		self.curr_pos = -1
		self.curr_file = ""

		self.static_routes = {}

		self.advance()
		self.scan()

	def advance(self):
		self.curr_pos += 1

		if self.curr_pos >= self.src_length:
			self.curr_char = '\0'

		else:
			self.curr_char = self.src[self.curr_pos]

	def scan(self):
		while self.curr_char != '\0':
			
			if self.curr_char == '\"':
				temp = ""
				self.advance()

				while self.curr_char.isalpha() or self.curr_char == '.':
					temp += self.curr_char
					self.advance()

				self.determine_static_file_type(temp)

			self.advance()

	def determine_static_file_type(self, file):
		if "." in file:
			file_type = file.split(".")[1]

			if file_type == "css":
				self.stylesheet()
				def static(response):
					response.header = [('Content-type', 'text/css')]
					response.render_static_file(self.curr_file)

	def stylesheet(self):
		def callback(cb):
			self.static_routes[file] = cb
			return cb

		return callback

	def return_static_routes(self):
		return self.static_routes
