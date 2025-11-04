from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from database import get_tasks, create_task, update_task_status, delete_task

app = FastAPI(
    title="Gerenciador de Tarefas Simples",
    description="Um aplicativo CRUD de tarefas completo com FastAPI, Jinja e SQLite.",
    version="0.1.0"
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    tasks = get_tasks()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


@app.post("/tasks", response_class=RedirectResponse)
async def add_task(request: Request, description: str = Form(...)):
    if description and description.strip():
        create_task(description.strip())
    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/complete", response_class=RedirectResponse)
async def toggle_complete_task(task_id: int, request: Request, completed: str = Form(...)):
    is_completed = completed.lower() == 'true'
    update_task_status(task_id, is_completed)
    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/delete", response_class=RedirectResponse)
async def remove_task(task_id: int, request: Request):
    delete_task(task_id)
    return RedirectResponse(url="/", status_code=303)
