import json
import logging

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from config import settings
from logger.common import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
storage: str = settings.file_name


class Task(BaseModel):
    id: int
    title: str
    status: bool


def load_tasks(folder: str) -> list:
    logging.info('open tasks folder for read')
    try:
        with open(folder, 'r', encoding='utf-8') as file_r:
            data = json.load(file_r)
    except (IOError, json.JSONDecodeError) as e:
        logging.warning('Exception %s', e)
        return []
    else:
        logging.info('return data')
        return data


def save_tasks(folder: str, tasks: list) -> None:
    logging.info('open tasks folder for write')
    try:
        with open(folder, 'w', encoding='utf-8') as file_w:
            json.dump(tasks, file_w, indent=4)
    except IOError as e:
        logging.error('Exception %s', e)


def get_task_id():
    logging.info('get task id')
    tasks = load_tasks(storage)
    logging.info(tasks)
    if not tasks:
        return 1
    max_id = max(task['id'] for task in tasks)
    logging.info('max task id: %s', max_id)
    next_id = max_id + 1
    logging.info('next task id: %s', next_id)
    return next_id


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    logging.info('all task status True')
    tasks = load_tasks(storage)
    task_all = [task for task in tasks if task['status']]
    return task_all


@app.post("/tasks", response_model=Task)
def create_task(title: str):
    logging.info('create task')
    id = get_task_id()
    task = {'id': id,
            'title': title,
            'status': True}
    tasks = load_tasks(storage)
    tasks.append(task)
    save_tasks(storage, tasks)
    logging.info('task id: %s title: %s done', id, title)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, title: str):
    logging.info(msg=f'change title task {task_id = }')
    tasks = load_tasks(storage)
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['title'] = title
        save_tasks(storage, tasks)
        logging.info(msg=f'good title task {task_id = } is change {title = }')
        return task
    else:
        logging.warning(f'Task with id {task_id} not found')
        return {"detail": "Task not found"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    logging.info('delete task id: %s', task_id)
    tasks = load_tasks(storage)
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['status'] = False
        save_tasks(storage, tasks)
        logging.info('task id: %s deleted', task_id)
        return {"detail": "Task deleted"}
    else:
        logging.warning(f'Task with id {task_id} not found')
        return {"detail": "Task not found"}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='localhost', port=8000, reload=True)
