-- 任務管理系統 - SQLite 資料庫建表語法
-- 版本：v1.0
-- 建立日期：2026-04-15

-- 建立任務資料表
CREATE TABLE IF NOT EXISTS tasks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    description  TEXT,
    is_done      INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    completed_at TEXT
);

-- 建立索引：加速依完成狀態篩選
CREATE INDEX IF NOT EXISTS idx_tasks_is_done ON tasks (is_done);
