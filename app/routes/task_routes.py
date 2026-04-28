from flask import Blueprint, render_template, request, redirect, url_for

# 定義任務模組的 Blueprint
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/')
def index():
    """
    顯示任務列表。
    可透過 query parameter 'filter' 過濾任務狀態。
    """
    pass

@task_bp.route('/add', methods=['POST'])
def add_task():
    """
    新增一個任務。
    接收 POST 請求中的 title 欄位。
    """
    pass

@task_bp.route('/toggle/<int:id>', methods=['POST'])
def toggle_task(id):
    """
    切換指定任務的完成狀態。
    接收 ID 作為 URL 參數。
    """
    pass

@task_bp.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    """
    刪除指定任務。
    接收 ID 作為 URL 參數。
    """
    pass
