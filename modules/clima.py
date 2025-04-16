import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str) -> dict:
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("API key não configurada no .env")
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt"
        response = requests.get(url)
        data = response.json()
        
        if data.get('cod') != 200:
            error_msg = data.get('message', 'Erro desconhecido na API')
            return {'error': f"Erro na API: {error_msg}"}
        
        return {
            'temperatura': data['main']['temp'],
            'descricao': data['weather'][0]['description'],
            'cidade': data['name']
        }
        
    except Exception as e:
        return {'error': f"Falha na requisição: {str(e)}"}

