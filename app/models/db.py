import sqlite3
import os

DATABASE_PATH = os.path.join(os.getcwd(), 'instance', 'database.db')

def get_db_connection():
    """建立並回傳資料庫連線"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # 允許透過欄位名稱存取資料
    return conn

def init_db():
    """根據 schema.sql 初始化資料庫"""
    if not os.path.exists(os.path.dirname(DATABASE_PATH)):
        os.makedirs(os.path.dirname(DATABASE_PATH))
    
    schema_path = os.path.join(os.getcwd(), 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    conn = get_db_connection()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
