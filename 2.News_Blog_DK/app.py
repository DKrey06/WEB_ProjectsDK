from flask import Flask

app= Flask(__name__)

@app.route("/")
def index():
	return "<h1>Добро пожаловать в Новостной Блог!</h1>"

@app.route("/about")
def about():
	return "<h1>about us</h1>"

@app.route("/contact")
def contact():
	return "<h1>contact</h1>"

if __name__ == '__main__':
	app.run(debug=True)