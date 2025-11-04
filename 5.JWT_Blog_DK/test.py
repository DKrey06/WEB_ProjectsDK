import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_jwt_auth():
    print("=== Тестирование JWT авторизации ===\n")

    print("1. Получение токенов...")
    login_data = {
        'email': 'mrdmitry2006@mail.ru',
        'password': '123456'
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        
        print(f"\nAccess Token: {access_token[:50]}...")
        print(f"Refresh Token: {refresh_token[:50]}...")
        
        print("\n2. Обновление access токена...")
        headers = {
            'Authorization': f'Bearer {refresh_token}'
        }
        
        refresh_response = requests.post(f"{BASE_URL}/api/auth/refresh", headers=headers)
        print(f"Статус: {refresh_response.status_code}")
        print(f"Ответ: {json.dumps(refresh_response.json(), indent=2, ensure_ascii=False)}")
        
        if refresh_response.status_code == 200:
            new_tokens = refresh_response.json()
            new_access_token = new_tokens['access_token']
            print(f"\nНовый Access Token: {new_access_token[:50]}...")
            
            print("\n3. Тестируем доступ к защищенному API...")
            protected_headers = {
                'Authorization': f'Bearer {new_access_token}'
            }
            
            articles_response = requests.get(f"{BASE_URL}/api/articles", headers=protected_headers)
            print(f"Статус получения статей: {articles_response.status_code}")
            
    else:
        print("Ошибка авторизации!")

if __name__ == "__main__":
    test_jwt_auth()