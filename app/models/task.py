import sqlite3
from datetime import datetime

DB_PATH = "database/tasks.db"


def get_connection():
    """建立並回傳 SQLite 資料庫連線。"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可用欄位名稱存取
    return conn


def init_db():
    """初始化資料庫，執行 schema.sql 建立資料表。"""
    with get_connection() as conn:
        with open("database/schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())


# ──────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────

def create(title: str, description: str = None) -> int:
    """
    新增一筆任務。

    Args:
        title: 任務名稱（必填）
        description: 任務描述（選填）

    Returns:
        新增任務的 id
    """
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    sql = """
        INSERT INTO tasks (title, description, is_done, created_at)
        VALUES (?, ?, 0, ?)
    """
    with get_connection() as conn:
        cursor = conn.execute(sql, (title.strip(), description, now))
        conn.commit()
        return cursor.lastrowid


# ──────────────────────────────────────────
# READ
# ──────────────────────────────────────────

def get_all(filter: str = "all") -> list:
    """
    取得所有任務，可依完成狀態篩選。

    Args:
        filter: "all" | "pending" | "completed"

    Returns:
        任務列表（sqlite3.Row 物件）
    """
    if filter == "pending":
        sql = "SELECT * FROM tasks WHERE is_done = 0 ORDER BY created_at DESC"
    elif filter == "completed":
        sql = "SELECT * FROM tasks WHERE is_done = 1 ORDER BY completed_at DESC"
    else:
        sql = "SELECT * FROM tasks ORDER BY created_at DESC"

    with get_connection() as conn:
        return conn.execute(sql).fetchall()


def get_by_id(task_id: int):
    """
    依 id 取得單一任務。

    Args:
        task_id: 任務 id

    Returns:
        sqlite3.Row 物件，若不存在則回傳 None
    """
    sql = "SELECT * FROM tasks WHERE id = ?"
    with get_connection() as conn:
        return conn.execute(sql, (task_id,)).fetchone()


# ──────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────

def toggle_complete(task_id: int) -> bool:
    """
    切換任務的完成狀態。
    - 待辦中 → 已完成：記錄 completed_at
    - 已完成 → 待辦中：清除 completed_at

    Args:
        task_id: 任務 id

    Returns:
        True 若成功，False 若任務不存在
    """
    task = get_by_id(task_id)
    if task is None:
        return False

    if task["is_done"] == 0:
        # 標記完成
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        sql = "UPDATE tasks SET is_done = 1, completed_at = ? WHERE id = ?"
        params = (now, task_id)
    else:
        # 取消完成
        sql = "UPDATE tasks SET is_done = 0, completed_at = NULL WHERE id = ?"
        params = (task_id,)

    with get_connection() as conn:
        conn.execute(sql, params)
        conn.commit()
    return True


def update(task_id: int, title: str = None, description: str = None) -> bool:
    """
    更新任務的名稱或描述。

    Args:
        task_id: 任務 id
        title: 新的任務名稱（選填）
        description: 新的任務描述（選填）

    Returns:
        True 若成功，False 若任務不存在
    """
    task = get_by_id(task_id)
    if task is None:
        return False

    new_title = title.strip() if title else task["title"]
    new_description = description if description is not None else task["description"]

    sql = "UPDATE tasks SET title = ?, description = ? WHERE id = ?"
    with get_connection() as conn:
        conn.execute(sql, (new_title, new_description, task_id))
        conn.commit()
    return True


# ──────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────

def delete(task_id: int) -> bool:
    """
    刪除指定任務。

    Args:
        task_id: 任務 id

    Returns:
        True 若成功，False 若任務不存在
    """
    task = get_by_id(task_id)
    if task is None:
        return False

    sql = "DELETE FROM tasks WHERE id = ?"
    with get_connection() as conn:
        conn.execute(sql, (task_id,))
        conn.commit()
    return True
