from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User

def jwt_middleware():    
    if request.method == 'OPTIONS':
        return None
    
    protected_endpoints = {
        'api_create_article',      # POST /api/articles
        'api_update_article',      # PUT /api/articles/1
        'api_delete_article',      # DELETE /api/articles/1
        'api_create_comment',      # POST /api/comment
        'api_update_comment',      # PUT /api/comment/1
        'api_delete_comment',      # DELETE /api/comment/1
        'api_verify_token',        # POST /api/auth/verify
    }
    
    refresh_endpoints = {
        'api_refresh'              # POST /api/auth/refresh
    }
    
    if not request.endpoint:
        return
    
    if request.endpoint in refresh_endpoints:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Refresh токен отсутствует'
            }), 401
        
        try:
            verify_jwt_in_request(refresh=True)
            current_user_id = get_jwt_identity()
            
            user = User.query.get(current_user_id)
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'Пользователь не найден'
                }), 401
            
            request.current_user = user
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Неверный refresh токен: {str(e)}'
            }), 422
    
    elif request.endpoint in protected_endpoints:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Access токен отсутствует'
            }), 401
        
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            
            user = User.query.get(current_user_id)
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'Пользователь не найден'
                }), 401
            
            request.current_user = user
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Неверный access токен: {str(e)}'
            }), 422