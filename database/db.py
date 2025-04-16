# integração do Banco de Dados com o Python

import mysql.connector # Importa o módulo mysql.connector para conectar ao MySQL
from dotenv import load_dotenv # Importa o módulo load_dotenv para carregar variáveis de ambiente
import os # Importa o módulo os para acessar variáveis de ambiente

load_dotenv()  # Carregar as variáveis de ambiente do arquivo .env

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),  # Obtém o host do banco de dados do arquivo .env
        user=os.getenv('DB_USER'),  # Obtém o usuário do banco de dados do arquivo .env
        password=os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados do arquivo .env
        database=os.getenv('DB_NAME')  # Obtém o nome do banco de dados do arquivo .env
    )