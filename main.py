# main.py
from modules.clima import get_weather

if __name__ == "__main__":
    cidade = input("Digite a cidade: ")
    try:
        dados = get_weather(cidade)
        if dados.get("cod") != 200:  # Se a API retornar erro
            print(f"Erro: {dados.get('message', 'Cidade não encontrada')}")
        else:
            print(f"Temperatura: {dados['main']['temp']}°C")
    except Exception as e:
        print(f"Erro ao acessar a API: {e}")