from flask import Flask, render_template, request
import re

app= Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/contact")
def contact():
	return render_template('contact.html')

@app.route("/feedback", methods=['POST','GET'])
def feedback():
	if request.method == 'POST':
		username = request.form.get('username', '').strip()
		usermail = request.form.get('usermail', '').strip()
		textmess = request.form.get('textmess', '').strip()
		errors={}

		if not username:
			errors['username'] = 'Обязательно введите имя'
		if not usermail:
			errors['usermail'] = 'Обязательно введите email'
		else:
			email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
			if not re.match(email_pattern, usermail):
				errors['usermail'] = 'Введите корректный email адрес'
		if not textmess:
			errors['textmess'] = 'Обязательно введите сообщение'
		
		if errors:
			return render_template('feedback.html', errors=errors,username=username,usermail=usermail,textmess=textmess)
		
		return render_template('post_feedback.html', errors=errors,username=username,usermail=usermail,textmess=textmess)
	else:
		return render_template('feedback.html')

if __name__ == '__main__':
	app.run(debug=True)