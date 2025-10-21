from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from models import db, Article, Comment
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/articles', methods=['GET'])
def get_articles():
    articles = Article.query.order_by(Article.created_date.desc()).all()
    
    articles_list = []
    for article in articles:
        articles_list.append({
            'id': article.id,
            'title': article.title,
            'text': article.text,
            'category': article.category,
            'created_date': article.created_date.isoformat(),
            'author': article.author.name,
            'author_id': article.author.id
        })
    
    return jsonify({
    'success': True,
    'count': len(articles_list),
    'articles': articles_list
})

@api_bp.route('/api/articles/<int:id>', methods=['GET'])
def get_article(id):
    article = Article.query.get(id)
    
    if not article:
        return jsonify({
            'success': False,
            'error': f'Статья с ID {id} не найдена'
        })
    
    article_data = {
        'id': article.id,
        'title': article.title,
        'text': article.text,
        'category': article.category,
        'created_date': article.created_date.isoformat(),
        'author': article.author.name,
        'author_id': article.author.id
    }
    
    return jsonify({
    'success': True,
    'article': article_data
})