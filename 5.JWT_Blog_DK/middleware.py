from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User

def jwt_middleware():    
    protected_endpoints = {
        'api_create_article',      # POST /api/articles
        'api_update_article',      # PUT /api/articles/1
        'api_delete_article',      # DELETE /api/articles/1
        'api_create_comment',      # POST /api/comment
        'api_update_comment',      # PUT /api/comment/1
        'api_delete_comment',      # DELETE /api/comment/1
        'api_refresh'              # POST /api/auth/refresh
    }
    
    if not request.endpoint or request.endpoint not in protected_endpoints:
        return
    
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({
            'success': False,
            'error': 'Токен отсутствует. Используйте: Bearer <token>'
        }), 401
    
    verify_jwt_in_request()
    current_user_id = get_jwt_identity()
    
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({
            'success': False,
            'error': 'Пользователь не найден'
        }), 401
    
    request.current_user = user