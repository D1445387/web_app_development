import sqlite3
import os

# 預設資料庫路徑 (對應到 instance/database.db)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線"""
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Task:
    @staticmethod
    def create(title):
        """新增任務"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, status) VALUES (?, 0)", (title,))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return task_id

    @staticmethod
    def get_all(filter_status=None):
        """取得任務清單，支援狀態篩選"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if filter_status == 'done':
            cursor.execute("SELECT * FROM tasks WHERE status = 1 ORDER BY created_at DESC")
        elif filter_status == 'todo':
            cursor.execute("SELECT * FROM tasks WHERE status = 0 ORDER BY created_at DESC")
        else:
            cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            
        tasks = cursor.fetchall()
        conn.close()
        return [dict(task) for task in tasks]

    @staticmethod
    def get_by_id(task_id):
        """根據 ID 取得單一任務"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        conn.close()
        return dict(task) if task else None

    @staticmethod
    def update_status(task_id):
        """切換任務完成狀態"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = NOT status WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        """刪除任務"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
