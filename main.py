from modules.clima import get_weather

if  __name__ == "__main__":
    cidade = input("Digite o nome da cidade: ")
    dados = get_weather(cidade)
    print(f"Temperatura atual em {cidade}: {dados['main']['temp']}°C")
