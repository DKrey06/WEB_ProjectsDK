from flask import Flask, render_template, request
import re
from datetime import datetime, timedelta

app = Flask(__name__)

def get_articles():
    return [
        {
            'id': 1,
            'title': 'Статья 1',
            'date': datetime.now(),
            'preview': 'Описание статьи',
            'content': 'Какой-то мега крутой текст :)'
        },
        {
            'id': 2,
            'title': 'Статья 2',
            'date': datetime.now() - timedelta(days=1),
            'preview': 'Мега описание статейки',
            'content': 'Супер пупер текст'
        },
        {
            'id': 3,
            'title': 'Статья 3',
            'date': datetime.now() - timedelta(days=2),
            'preview': 'Нереальное превью статьи',
            'content': 'Уникальный текст про статью'
        },
        {
            'id': 4,
            'title': 'Статья 4',
            'date': datetime.now() ,
            'preview': 'Описание не придумали',
            'content': 'Текст статьи тоже не написали еще'
        },
        {
            'id': 5,
            'title': 'Статья 5',
            'date': datetime.now() - timedelta(days=15),
            'preview': 'Описательное описание',
            'content': 'Текстовый текст'
        }
    ]

@app.context_processor
def inject_today():
    return {'today': datetime.now().date()}



@app.route("/")
def index():
    articles = get_articles()
    return render_template('index.html', articles=articles)

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
        errors = {}

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
            return render_template('feedback.html', errors=errors, username=username, usermail=usermail, textmess=textmess)
        
        return render_template('post_feedback.html', errors=errors, username=username, usermail=usermail, textmess=textmess)
    else:
        return render_template('feedback.html')

@app.route('/news/<int:id>')
def news(id):
    articles = get_articles()
    article = next((article for article in articles if article['id'] == id), None)
    
    if article is None:
        return "Статья не найдена", 404
    
    return render_template('news_detail.html', article=article)

if __name__ == '__main__':
    app.run(debug=True)