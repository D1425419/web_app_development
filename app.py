import os
import sqlite3
from flask import Flask
from app.routes.book_routes import book_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
# 載入環境變數設定
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# 確保必要的目錄存在
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
os.makedirs(os.path.join(app.static_folder, 'uploads'), exist_ok=True)

# 註冊路由 Blueprint
app.register_blueprint(book_bp)

def init_db():
    """初始化資料庫與資料表"""
    db_path = os.path.join(app.root_path, 'instance', 'database.db')
    schema_path = os.path.join(app.root_path, 'database', 'schema.sql')
    
    conn = sqlite3.connect(db_path)
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("資料庫初始化完成！")

if __name__ == '__main__':
    # 啟動時自動初始化資料庫（MVP 階段方便測試）
    init_db()
    app.run(debug=True)
