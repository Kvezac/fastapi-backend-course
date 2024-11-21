import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/tasks")
def get_tasks():
    pass


@app.post("/tasks")
def create_task(task):
    pass


@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    pass


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    pass


if __name__ == '__main__':
    uvicorn.run(app=app, host='localhost', port=8000)
