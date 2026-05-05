import sqlite3
import os
from flask import current_app, g

def get_db_connection():
    """
    建立並回傳資料庫連線。
    使用 Flask 的 g 物件來確保在同一個 request 中重複使用同一個連線。
    """
    if 'db' not in g:
        # 優先使用 Flask 配置中的 DATABASE 路徑
        db_path = current_app.config.get('DATABASE')
        if not db_path:
            db_path = os.path.join(os.getcwd(), 'instance', 'database.db')
            
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row  # 允許透過欄位名稱存取資料
        
    return g.db

def close_db(e=None):
    """關閉資料庫連線"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    根據 schema.sql 初始化資料庫。
    """
    db_path = current_app.config['DATABASE']
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    
    # 假設 schema.sql 在專案根目錄的 database 資料夾下
    schema_path = os.path.join(current_app.root_path, '..', 'database', 'schema.sql')
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    db = get_db_connection()
    db.executescript(schema_sql)
    db.commit()
