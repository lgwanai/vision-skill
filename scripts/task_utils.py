import os
import json
import uuid
from datetime import datetime

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.tasks')

if not os.path.exists(TASKS_DIR):
    os.makedirs(TASKS_DIR)

def create_task(task_type, params):
    """创建新任务"""
    task_id = str(uuid.uuid4())
    task_data = {
        "id": task_id,
        "type": task_type,
        "params": params,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "result": None,
        "error": None
    }
    save_task(task_id, task_data)
    return task_id

def get_task(task_id):
    """获取任务信息"""
    task_file = os.path.join(TASKS_DIR, f"{task_id}.json")
    if not os.path.exists(task_file):
        return None
    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"id": task_id, "status": "error", "error": f"读取任务文件失败: {str(e)}"}

def update_task(task_id, updates):
    """更新任务信息"""
    task = get_task(task_id)
    if not task:
        return False
    
    task.update(updates)
    task['updated_at'] = datetime.now().isoformat()
    save_task(task_id, task)
    return True

def save_task(task_id, data):
    """保存任务信息到文件"""
    task_file = os.path.join(TASKS_DIR, f"{task_id}.json")
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
