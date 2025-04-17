import requests
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

class CurrencyConverter:
    def __init__(self):
        self.api_key = os.getenv("EXCHANGERATE_API_KEY")
        self.db_connection = self._create_db_connection()

    def _create_db_connection(self):
        """Cria conexão com o MySQL"""
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except Exception as e:
            print(f"Erro ao conectar ao banco: {e}")
            return None

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """Obtém a taxa de câmbio atual da API"""
        try:
            url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair/{from_currency}/{to_currency}"
            response = requests.get(url)
            data = response.json()
            
            if data.get("result") == "success":
                return data.get("conversion_rate", 0)
            else:
                print(f"Erro na API: {data.get('error-type', 'Erro desconhecido')}")
                return 0
                
        except Exception as e:
            print(f"Erro na requisição: {e}")
            return 0

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> dict:
        """Realiza a conversão e salva no histórico"""
        rate = self.get_exchange_rate(from_currency, to_currency)
        if rate == 0:
            return {"error": "Não foi possível obter a taxa de câmbio"}
        
        converted_amount = amount * rate
        
        # Salva no histórico
        self._save_conversion_history(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            converted_amount=converted_amount,
            rate=rate
        )
        
        return {
            "original_amount": amount,
            "converted_amount": converted_amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "rate": rate,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def _save_conversion_history(self, from_currency: str, to_currency: str, 
                               amount: float, converted_amount: float, rate: float) -> bool:
        """Armazena a conversão no banco de dados"""
        if not self.db_connection:
            return False
            
        try:
            cursor = self.db_connection.cursor()
            query = """
                INSERT INTO historico_moedas 
                (moeda_origem, moeda_destino, valor_origem, valor_convertido, taxa_cambio)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (from_currency, to_currency, amount, converted_amount, rate))
            self.db_connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar no histórico: {e}")
            return False

    def get_conversion_history(self, limit: int = 10) -> list:
        """Recupera o histórico de conversões"""
        if not self.db_connection:
            return []
            
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = """
                SELECT * FROM historico_moedas
                ORDER BY data_conversao DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []