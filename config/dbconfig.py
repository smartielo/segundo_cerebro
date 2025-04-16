import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'cerebro_user'),
        password=os.getenv('DB_PASSWORD', '2808'),
        database=os.getenv('DB_NAME', 'segundo_cerebro'),
        auth_plugin='mysql_native_password'
    )