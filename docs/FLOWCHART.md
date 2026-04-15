# 流程圖文件（FLOWCHART）

**專案名稱：** 任務管理系統  
**文件版本：** v1.0  
**建立日期：** 2026-04-15  
**參考文件：** PRD.md

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
  A([使用者開啟網頁]) --> B[首頁 - 任務清單]

  B --> C{要執行什麼操作？}

  C -->|新增任務| D[輸入任務名稱]
  D --> E[點擊新增按鈕]
  E --> F{輸入是否有效？}
  F -->|是| G[儲存至資料庫]
  G --> B
  F -->|否| H[顯示錯誤提示]
  H --> D

  C -->|標記完成| I[點擊完成按鈕]
  I --> J[切換任務狀態為已完成]
  J --> B

  C -->|刪除任務| K[點擊刪除按鈕]
  K --> L[從資料庫移除]
  L --> B

  C -->|篩選任務| M{選擇篩選條件}
  M -->|全部| B
  M -->|待辦中| N[顯示未完成任務]
  M -->|已完成| O[顯示已完成任務]
  N --> C
  O --> C
```

---

## 2. 系統序列圖（System Sequence Diagram）

描述各主要功能中，使用者、瀏覽器、Flask 後端與 SQLite 資料庫之間的互動流程。

### 2.1 新增任務

```mermaid
sequenceDiagram
  actor User as 使用者
  participant Browser as 瀏覽器
  participant Flask as Flask Route
  participant DB as SQLite

  User->>Browser: 輸入任務名稱並點擊「新增」
  Browser->>Flask: POST /tasks
  Flask->>Flask: 驗證輸入（非空、長度限制）
  alt 輸入有效
    Flask->>DB: INSERT INTO tasks (title, created_at)
    DB-->>Flask: 新增成功
    Flask-->>Browser: 302 重導向 GET /
    Browser->>Flask: GET /
    Flask->>DB: SELECT * FROM tasks
    DB-->>Flask: 回傳任務清單
    Flask-->>Browser: 渲染首頁（任務清單更新）
  else 輸入無效
    Flask-->>Browser: 顯示錯誤訊息（原頁面）
  end
```

### 2.2 標記任務完成

```mermaid
sequenceDiagram
  actor User as 使用者
  participant Browser as 瀏覽器
  participant Flask as Flask Route
  participant DB as SQLite

  User->>Browser: 點擊任務的「完成」按鈕
  Browser->>Flask: POST /tasks/<id>/complete
  Flask->>DB: UPDATE tasks SET is_done=1, completed_at=NOW() WHERE id=<id>
  DB-->>Flask: 更新成功
  Flask-->>Browser: 302 重導向 GET /
  Browser->>Flask: GET /
  Flask->>DB: SELECT * FROM tasks
  DB-->>Flask: 回傳任務清單
  Flask-->>Browser: 渲染首頁（任務狀態更新）
```

### 2.3 刪除任務

```mermaid
sequenceDiagram
  actor User as 使用者
  participant Browser as 瀏覽器
  participant Flask as Flask Route
  participant DB as SQLite

  User->>Browser: 點擊任務的「刪除」按鈕
  Browser->>Flask: POST /tasks/<id>/delete
  Flask->>DB: DELETE FROM tasks WHERE id=<id>
  DB-->>Flask: 刪除成功
  Flask-->>Browser: 302 重導向 GET /
  Browser->>Flask: GET /
  Flask->>DB: SELECT * FROM tasks
  DB-->>Flask: 回傳任務清單
  Flask-->>Browser: 渲染首頁（任務移除）
```

### 2.4 篩選任務

```mermaid
sequenceDiagram
  actor User as 使用者
  participant Browser as 瀏覽器
  participant Flask as Flask Route
  participant DB as SQLite

  User->>Browser: 點擊篩選按鈕（全部 / 待辦中 / 已完成）
  Browser->>Flask: GET /?filter=all | pending | completed
  Flask->>DB: SELECT * FROM tasks WHERE ... (依篩選條件)
  DB-->>Flask: 回傳符合條件的任務清單
  Flask-->>Browser: 渲染首頁（顯示篩選結果）
```

---

## 3. 功能清單對照表

| 功能編號 | 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
|----------|----------|----------|-----------|------|
| F-01 | 顯示任務清單 | `/` | GET | 首頁，顯示所有任務 |
| F-02 | 依狀態篩選 | `/?filter=<all\|pending\|completed>` | GET | Query String 控制篩選條件 |
| F-03 | 新增任務 | `/tasks` | POST | 接收表單資料，建立新任務 |
| F-04 | 標記任務完成 | `/tasks/<id>/complete` | POST | 切換指定任務的完成狀態 |
| F-05 | 刪除任務 | `/tasks/<id>/delete` | POST | 刪除指定任務 |

> 💡 **設計說明：** 由於使用 HTML form，刪除與狀態切換統一使用 POST 方法，避免瀏覽器直接呼叫 GET 造成誤操作。

---

## 4. 頁面狀態說明

| 頁面狀態 | 觸發條件 | 顯示內容 |
|----------|----------|----------|
| 預設（全部） | `GET /` 或 `GET /?filter=all` | 所有任務清單 |
| 待辦中篩選 | `GET /?filter=pending` | `is_done = 0` 的任務 |
| 已完成篩選 | `GET /?filter=completed` | `is_done = 1` 的任務 |
| 新增成功 | POST /tasks 成功後 | 重導向首頁，任務清單更新 |
| 輸入錯誤 | POST /tasks 驗證失敗 | 首頁顯示錯誤提示訊息 |
