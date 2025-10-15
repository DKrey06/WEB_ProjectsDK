from flask import Flask, render_template, request, flash, url_for, redirect
import re
from datetime import datetime, timedelta
from models import db, User, Article
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_blog_DK.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456'

db.init_app(app)

def init_db():
    with app.app_context():
        db.create_all() 

        test_user = User.query.filter_by(email='mrdmitry2006@mail.ru').first()
        if not test_user:
            test_user = User(
                name='Дмитрий Кретов', 
                email='mrdmitry2006@mail.ru',
                hashed_password=generate_password_hash('123456')
            )
            db.session.add(test_user)
            db.session.commit()
        
        if Article.query.count() == 0:
            articles_data = [
                {
                    'title': 'Первая новость',
                    'text': 'Текст первой новости'
                },
                {
                    'title': 'Вторая новость',
                    'text': 'Текст второй новости'
                },
                {
                    'title': 'Третья новость', 
                    'text': 'Текст третьей новости'
                }
            ]
                
            for article_data in articles_data:
                article = Article(
                    title=article_data['title'],
                    text=article_data['text'],
                    author=test_user,
                    created_date=datetime.now()
                )
                db.session.add(article)
            
            db.session.commit()

def get_articles():
    articles_from_db = Article.query.order_by(Article.created_date.desc()).all()
    
    articles = []
    for article in articles_from_db:
        articles.append({
            'id': article.id,
            'title': article.title,
            'date': article.created_date,
            'preview': article.text[:100] + '...' if len(article.text) > 100 else article.text,
            'content': article.text,
            'author': article.author.name
        })
    
    return articles

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
    article = Article.query.get_or_404(id)
    
    article_data = {
        'id': article.id,
        'title': article.title,
        'date': article.created_date,
        'preview': article.text[:100] + '...' if len(article.text) > 100 else article.text,
        'content': article.text,
        'author': article.author.name
    }
    
    return render_template('news_detail.html', article=article_data)

@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        text = request.form.get('text', '').strip()
        errors = {}

        if not title:
            errors['title'] = 'Обязательно введите заголовок'
        if not text:
            errors['text'] = 'Обязательно введите текст статьи'

        if errors:
            return render_template('create_article.html', errors=errors, title=title, text=text)

        author = User.query.first()
        if not author:
            flash('В базе данных нет пользователей', 'error')
            return render_template('create_article.html', title=title, text=text)
        
        article = Article(
            title=title,
            text=text,
            author=author,
            created_date=datetime.now()
        )

        db.session.add(article)
        db.session.commit()
        flash('Статья создана!', 'success')
        return redirect(url_for('index'))

    return render_template('create_article.html')

@app.route('/edit-article/<int:id>', methods=['POST', 'GET'])
def edit_article(id):
    article = Article.query.get_or_404(id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        text = request.form.get('text', '').strip()
        errors = {}

        if not title:
            errors['title'] = 'Обязательно введите заголовок'
        if not text:
            errors['text'] = 'Обязательно введите текст статьи'

        if errors:
            return render_template('edit_article.html', errors=errors, title=title, text=text, article=article)

        article.title = title
        article.text = text
        
        db.session.commit()
        return redirect(url_for('news', id=article.id))

    return render_template('edit_article.html', article=article)

@app.route('/delete-article/<int:id>', methods=['POST'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)