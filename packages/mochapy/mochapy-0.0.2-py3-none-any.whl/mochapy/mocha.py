from wsgiref.simple_server import make_server
from mocha_response import Response
from mocha_request import Request
from mocha_scanner import Scanner

class Mocha:
	def __init__(self):
		self.__get_routes = {}
		self.__static_routes = {}
		self.__views_directory = ""
		self.__static_directory = ""

	def __call__(self, environment, start_response):
		request = Request(environment)
		response = self.__request_handler(request, start_response)

		print("hi")

		return [bytes(response)]

	def __request_handler(self, request, start_response):
		response = Response(start_response, self.__views_directory, self.__static_directory)
		response.header = [('Content-type', 'text/html')]
		response.status = "200 OK"

		for path, cb in self.__get_routes.items():
			if path == request.path():
				cb(response)

				return response

	def set(self, setting_name, setting):
		if setting_name == "views":
			self.__views_directory = setting

		if setting_name == "static":
			self.__static_directory = setting

	def get(self, path):
		def callback(cb):
			self.__get_routes[path] = cb
			return cb

		return callback

	def listen(self, port):
		def callback(cb):
			cb()
			with make_server('', port, self) as server:
				server.serve_forever()

		return callback
			