from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task

# 定義任務模組的 Blueprint
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/')
def index():
    """
    顯示任務列表。
    可透過 query parameter 'filter' 過濾任務狀態。
    """
    filter_status = request.args.get('filter')
    tasks = Task.get_all(filter_status)
    return render_template('index.html', tasks=tasks, current_filter=filter_status)

@task_bp.route('/add', methods=['POST'])
def add_task():
    """
    新增一個任務。
    接收 POST 請求中的 title 欄位，並進行基本驗證。
    """
    title = request.form.get('title', '').strip()
    
    if not title:
        flash('任務標題不能為空！', 'danger')
        return redirect(url_for('tasks.index'))
    
    task_id = Task.create(title)
    if task_id:
        flash('任務已成功新增！', 'success')
    else:
        flash('新增任務時發生錯誤。', 'danger')
        
    return redirect(url_for('tasks.index'))

@task_bp.route('/toggle/<int:id>', methods=['POST'])
def toggle_task(id):
    """
    切換指定任務的完成狀態。
    接收 ID 作為 URL 參數。
    """
    if Task.toggle_status(id):
        flash('任務狀態已更新！', 'success')
    else:
        flash('更新任務狀態失敗。', 'danger')
        
    return redirect(url_for('tasks.index'))

@task_bp.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    """
    刪除指定任務。
    接收 ID 作為 URL 參數。
    """
    if Task.delete(id):
        flash('任務已刪除！', 'info')
    else:
        flash('刪除任務失敗。', 'danger')
        
    return redirect(url_for('tasks.index'))
