import requests
api_key = "sua_chave"
response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=Bauru&appid={api_key}")
print(response.status_code)  # Deve retornar 200
print(response.json())  # Mostra os dados brutos