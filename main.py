from modules.clima import get_weather

if __name__ == "__main__":
    cidade = input("Digite a cidade: ")
    dados = get_weather(cidade)
    
    if 'error' in dados:
        print(f"❌ {dados['error']}")
        if "Invalid API key" in dados['error']:
            print("👉 Solução: Verifique sua API key no arquivo .env")
    else:
        print(f"🌤 Clima em {dados['cidade']}:")
        print(f"🌡 Temperatura: {dados['temperatura']}°C")
        print(f"📌 Condição: {dados['descricao'].capitalize()}")