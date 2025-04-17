import requests
import os
from dotenv import load_dotenv
from datetime import datetime  

load_dotenv()

def get_weather(city: str) -> dict:
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt"
        response = requests.get(url)
        data = response.json()
        
        if data.get('cod') != 200:
            return {'error': data.get('message', 'Erro na API')}
        
        return {
            'cidade': data['name'],
            'temperatura': data['main']['temp'],
            'descricao': data['weather'][0]['description'].capitalize(),
            'umidade': data['main']['humidity'],
            'vento': data['wind']['speed'],
            'nascer_do_sol': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
            'por_do_sol': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        }
        
    except Exception as e:
        return {'error': str(e)}
