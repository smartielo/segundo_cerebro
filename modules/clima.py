# modulo de clima
import requests
import os
from dotenv import load_dotenv # Carregar variáveis de ambiente do arquivo .env

load_dotenv() # Carregar as variáveis de ambiente

def get_weather(city: str) -> dict: # Obtém o clima atual de uma cidade
    api_key = os.getenv('WEATHER_API_KEY') # Obtém a chave da API do arquivo .env
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt" # URL da API
    response = requests.get(url) # Faz a requisição para a API
return response.json() # Retorna a resposta em formato JSON

#exemplo de uso
#clima = get_weather("São Paulo")
#print(clima["main"]["temp"]) # imprime a temperatura atual



