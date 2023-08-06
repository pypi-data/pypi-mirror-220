from mocha import Mocha
import sys

app = Mocha()

app.set("views", "views/")
app.set("static", "public/")

@app.get("/")
def index(response):
	response.render("index.html")

@app.get("/style.css")
def style(response):
	response.header = [('Content-type', 'text/css')]
	response.render_static_file("style.css")

@app.listen(3000)
def start():
	print("Mocha server is up and running.")