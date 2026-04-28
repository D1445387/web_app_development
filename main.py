import os
import sqlite3
from flask import Flask
from app.routes.task_routes import task_bp

def create_app():
    # 初始化 Flask 應用程式
    app = Flask(__name__, 
                instance_relative_config=True,
                template_folder='app/templates',
                static_folder='app/static')
    
    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 設定基本配置
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 註冊 Blueprint
    app.register_blueprint(task_bp)

    return app

# 初始化資料庫的函式
def init_db():
    db_path = os.path.join('instance', 'database.db')
    schema_path = os.path.join('database', 'schema.sql')
    
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
