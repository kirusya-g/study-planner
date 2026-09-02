from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from .database import engine
from . import models

model.Base.metadata.create_all(bind = engine)

#User(data that come from client)
class UserCreate(BaseModel):
    email: str
    nickname: str
    password: str
#User(data that we get back to client)
class User(BaseModel):
    id: int
    nickname: str
    email: str


#Calendar
class CalendarCreate(BaseModel):
    name: str
    color: str

class Calendar(BaseModel):
    id: int
    user_id: int
    name: str
    color: str


#Lesson
class LessonCreate(BaseModel):
    calendar_id : int
    name: str
    room: Optional[str] = None
    day_of_week: str
    time_start: str
    time_end: str
    descriptions: Optional[str] = None
    color: str = "#3498db"
    is_reccuring: bool = True
    links: List[str] = []
    files: List[str] = []

class Lesson(LessonCreate):
    id: int

#Task
class TaskCreate(BaseModel):
    calendar_id: int
    lesson_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    title: str
    descriprions: Optional[str] = None
    day: str
    time: Optional[str] = None
    deadline: Optional[str] = None
    color:  str = "#2ecc71"
    links: List[str] = []
    files: List[str] = []
    is_done: bool = False

class Task(TaskCreate):
    id: int

#Note
class NoteCreate(BaseModel):
    calendar_id: int
    day: str
    text: str

class Note(NoteCreate):
    id: int

#TEMPORARY STORAGE (instead of a database)
user: dict = {}
calendar: dict = {}
lesson: dict = {}
task: dict = {}
note: dict = {}

_counters = {
    "user": 0,
    "calendar": 0,
    "lesson": 0,
    "task": 0,
    "note": 0,
}

def next_id(entity: str) -> int:
    """Adds 1 to the counter of the given entity and returns the new number."""
    _counters[entity] += 1
    return _counters[entity]


app = FastAPI(title="Study Planner API")
@app.get("/")
def root():
    return {"message": "Study Planner API"}
#Users
@app.post("/users", response_model = User)
def create_user(data: UserCreate):
    user_id = next_id("user")
    user = {
        "id": user_id,
        "email": data.email,
        "nickname": data.nickname,
        "password": data.password, 
    }  
    user[user_id] = user
    return user

@app.get("/user/{user_id}", response_model = User)
def get_user(user_id: int):
    found_user = users.get(user_id)
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user

@app.put("/users/{user_id}", response_model = User)
def update_user(user_id: int, data: UserCreate):
    if user_id not in users:
        raise HTTPException(status_code = 404, detail = "User not found")

    updated_user = {"id": user_id, **data.model_dump()}
    users[user_id] = updated_user
    return updated_user

@app.delete("/users/{user_id}")
def detele_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code = 404, detail = "User not found")

    del users[user_id]
    return {"message": f"User {user_id} deleted"}

#Calendar
@app.post("/users/{user_id}/calendars/", response_model = Calendar)
def create_calendar(user_id: int, data: CalendarCreate):
    if user_id not in user:
        raise HTTPException(status_code = 404, detail = "User not found")
    cal_id = next_id("calendar")
    calendar = {"id": cal_id, "user_id": user_id, **data.model_dump()}
    calendar[cal_id] = calendar
    return calendar

@app.get("/users/{user_id}/calendars/", response_model = list[Calendar])
def list_calendar(user_id: int):
    return [c for c in calendar.values() if c["user_id"] == user_id]

@app.put("/users/{user_id}/calendars/{cal_id}", response_model = Calendar)
def update_calendar(user_id: int, cal_id: int, data: CalendarCreate):
    if cal_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calendar not found")
    if user_id not in users:
        raise HTTPException(status_code = 404, detail = "User not found")
    updated_calendar = {"id": cal_id, "user_id" : user_id, **data.model_dump()}
    calendars[cal_id] = updated_calendar
    return updated_calendar

@app.delete("/users/{user_id}/calendars/{cal_id}")
def delete_calendar(user_id: int, cal_id: int):
    if cal_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calendar not found")

    del calendars[cal_id]
    return {"message": f"Calendar {cal_id} deleted"}

#Lesson
@app.post("/calendars/{cal_id}/lessons/", response_model = Lesson)
def create_lesson(calendar_id: int, data: LessonCreate):
    if calendar_id not in calendar:
        raise HTTPException(status_code = 404, detail = "Calendar not found")
    les_id = next_id("lesson")
    lesson = {"id": les_id, **data.model_dump()}
    lesson[les_id] = lesson
    return lesson

@app.get("/user/{cal_id}/lessons/", response_model = list[Lesson])
def list_lesson(calendar_id: int):
    return [l for l in lesson.values() if l["calendar_id"] == calendar_id]

@app.put("/calendars/{cal_id}/lessons/{les_id}", response_model = Lesson)
def update_lesson(cal_id: int, les_id: int, data: LessonCreate):
    if les_id not in lessons:
        raise HTTPException(status_code = 404, detail = "Lesson not found")
    if cal_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calender not found")
    updated_lesson = {"id": les_id, "calendar_id": cal_id, **data.model_dump()}
    lessons[les_id] = updated_lesson
    return updated_lesson

@app.delete("/calendars/{cal_id}/lessons/{les_id}")
def delete_lesson(cal_id: int, les_id: int):
    if les_id not in lessons:
        raise HTTPException(status_code = 404, detail = "Lesson not found")
    
    del lessons[les_id]
    return {"message": f"Lesson {les_id} deleted"}



#Task
@app.post("/task", response_model = Task)
def create_task(data: TaskCreate):
    if data.calendar_id not in calendar:
        raise HTTPException(status_code = 404, detail = "Calendar not found")
    task_id = next_id("task")
    task = {"id": task_id, **data.model_dump()}
    task[task_id] = task
    return task

@app.get("/calendars/{calendar_id}/tasks/", response_model = list[Task])
def list_tasks(calendar_id: int):
    return [t for t in task.values() if t["calendar_id"] == calendar_id]

@app.patch("/tasks/{task_id}/toggle-done", response_model = Task)
def toggle_done(task_id: int):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code = 404, detail = "Task not found")
    task["is_done"] = not task["is_done"]
    return task

@app.put("/tasks/{task_id}", response_model = Task)
def update_task(task_id: int, data: TaskCreate):
    if task_id not in tasks:
        raise HTTPException(status_code = 404, detail = "Task not found")
    if data.calendar_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calendar not found")

    updated_task = {"id": task_id, **data.model_dump()}
    tasks[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code = 404, detail = "Task not found")

    del tasks[task_id]
    return {"message": f"Task {task_id} deleted"}


#Notes
@app.post("/notes", response_model = Note)
def create_notes(data: NoteCreate):
    if data.calendar_id not in calendar:
        raise HTTPException(status_code = 404, detail = "Calendar not found")
    note_id = next_id("note")
    note = {"id": note_id, **data.model_dump()}
    note[note_id] = note
    return note

@app.put("/notes/{note_id}", response_model = Note)
def update_note(note_id: int, data: NoteCreate):
    if note_id not in notes:
        raise HTTPException(status_code = 404, detail = "Note not found")

    if data.calendar_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calendar not found")
    updated_note = {"id": note_id, **data.model_dump()}
    note[note_id] = updated_note
    return updated_note

@app.delete("/notes/{note_id}")
def detele_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code = 404, detail = "Note not found")

    del note[note_id]
    return {"message": f"Note {note_id} deleted"}