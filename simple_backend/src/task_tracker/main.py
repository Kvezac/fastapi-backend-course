import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    status: bool


tasks: list[Task] = []


def get_task_id():
    logging.info('get task id')
    if not tasks:
        return 1
    id = max(tasks, key=lambda task: task['id'])
    logging.info('max task id: %s', id['id'])
    id = id['id'] + 1
    logging.info('next task id: %s', id)
    return id


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    logging.info('all task status True')
    task_all = [task for task in tasks if task['status']]
    return task_all


@app.post("/tasks", response_model=Task)
def create_task(title):
    logging.info('create task')
    id = get_task_id()
    task = {'id': id,
            'title': title,
            'status': True}
    tasks.append(task)
    logging.info('task id: %s title: %s done', id, title)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, title: str):
    logging.info(msg=f'change tittle task {task_id = }')
    task = [task for task in tasks if task['id'] == task_id][0]
    task['title'] = title
    logging.info(msg=f'good title task {task_id = } is change {title = }')
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    logging.info('delete task id: %s', task_id)
    task = [task for task in tasks if task['id'] == task_id][0]
    task['status'] = False
    logging.info('task id: %s deleted', task_id)
    return {"detail": "Task deleted"}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='localhost', port=8000, reload=True)
