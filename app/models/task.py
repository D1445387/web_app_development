import sqlite3
import os
from flask import current_app

# 資料庫路徑設定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """
    建立並取得資料庫連線。
    確保 instance 資料夾存在，並設定 row_factory。
    """
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"資料庫連線失敗: {e}")
        return None

class Task:
    @staticmethod
    def create(title):
        """
        新增一筆任務記錄。
        :param title: 任務標題
        :return: 建立成功的任務 ID
        """
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, status) VALUES (?, 0)", (title,))
            conn.commit()
            task_id = cursor.lastrowid
            return task_id
        except Exception as e:
            print(f"新增任務失敗: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all(filter_status=None):
        """
        取得所有任務記錄，支援狀態篩選。
        :param filter_status: 篩選條件 ('done' 或 'todo')
        :return: 任務字典列表
        """
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            if filter_status == 'done':
                cursor.execute("SELECT * FROM tasks WHERE status = 1 ORDER BY created_at DESC")
            elif filter_status == 'todo':
                cursor.execute("SELECT * FROM tasks WHERE status = 0 ORDER BY created_at DESC")
            else:
                cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            
            tasks = cursor.fetchall()
            return [dict(task) for task in tasks]
        except Exception as e:
            print(f"取得任務列表失敗: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(task_id):
        """
        根據 ID 取得單筆任務。
        :param task_id: 任務 ID
        :return: 任務字典或 None
        """
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            task = cursor.fetchone()
            return dict(task) if task else None
        except Exception as e:
            print(f"取得單筆任務失敗: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(task_id, data):
        """
        更新任務記錄。
        :param task_id: 任務 ID
        :param data: 包含更新欄位的字典 (如 {'title': '...', 'status': 1})
        """
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            keys = [f"{k} = ?" for k in data.keys()]
            values = list(data.values())
            values.append(task_id)
            query = f"UPDATE tasks SET {', '.join(keys)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"更新任務失敗: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def toggle_status(task_id):
        """
        切換任務的完成狀態。
        :param task_id: 任務 ID
        """
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status = NOT status WHERE id = ?", (task_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"切換任務狀態失敗: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(task_id):
        """
        刪除任務記錄。
        :param task_id: 任務 ID
        """
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"刪除任務失敗: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
