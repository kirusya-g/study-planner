from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models

models.Base.metadata.create_all(bind = engine)

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

    class Config:
        from_attributes = True


#Calendar
class CalendarCreate(BaseModel):
    name: str
    color: str

class Calendar(BaseModel):
    id: int
    user_id: int
    name: str
    color: str

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True

#Task
class TaskCreate(BaseModel):
    calendar_id: int
    lesson_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    title: str
    descriptions: Optional[str] = None
    day: str
    time: Optional[str] = None
    deadline: Optional[str] = None
    color:  str = "#2ecc71"
    links: List[str] = []
    files: List[str] = []
    is_done: bool = False

class Task(TaskCreate):
    id: int

    class Config:
        from_attributes = True

#Note
class NoteCreate(BaseModel):
    calendar_id: int
    day: str
    text: str

class Note(NoteCreate):
    id: int

    class Config:
        from_attributes = True

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
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        email = data.email,
        nickname = data.nickname,
        password = data.password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{user_id}", response_model = User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    return user

@app.put("/users/{user_id}", response_model = User)
def update_user(user_id: int, data: UserCreate, db = Session(User)):
    found_user = db.query(models.User).filter(models.User.id == user_id).first()
    if user_id not in users:
        raise HTTPException(status_code = 404, detail = "User not found")

    found_user.email = data.email
    found_user.nickname = data.nickname
    found_user.password = data.password

    db.commit()
    db.refresh(found_user)
    return found_user

@app.delete("/users/{user_id}")
def detele_user(user_id: int, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.id == user_id).first()
    if user_id not in users:
        raise HTTPException(status_code = 404, detail = "User not found")

    db.delete(found_user)
    db.commit()
    return {"message": f"User {user_id} deleted"}

#Calendar
@app.post("/users/{user_id}/calendars/", response_model = Calendar)
def create_calendar(user_id: int, data: CalendarCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user_id not in user:
        raise HTTPException(status_code = 404, detail = "User not found")
    new_calendar = models.Calendar(
        name = data.name,
        color = data.color,
        user_id = user_id,
    )
    db.add(new_calendar)
    db.commit()
    db.refresh(new_calendar)
    return new_calendar

@app.get("/users/{user_id}/calendars/", response_model = list[Calendar])
def list_calendar(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Calendar).filter(models.Calendar.User.id == user_id).all()

@app.put("/users/{user_id}/calendars/{cal_id}", response_model = Calendar)
def update_calendar(user_id: int, cal_id: int, data: CalendarCreate, db: Session = Depends(get_db)):
    calendar = db.query(models.Calendar).filter(models.Calendar.id == cal_id).first()
    if cal_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calendar not found")
    if user_id not in users:
        raise HTTPException(status_code = 404, detail = "User not found")

    calendar.name = data.name
    calendar.color = data.color
    calendar.user_id = user_id

    db.commit()
    db.refresh(calendar)
    return calendar

@app.delete("/users/{user_id}/calendars/{cal_id}")
def delete_calendar(user_id: int, cal_id: int, db: Session = Depends(get_db)):
    calendar = db.query(models.Calendar).filter(models.Calendar.id == cal_id).first()
    if cal_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calendar not found")

    db.delete(calendar)
    db.commit()
    return {"message": f"Calendar {cal_id} deleted"}

#Lesson
@app.post("/calendars/{cal_id}/lessons/", response_model = Lesson)
def create_lesson(calendar_id: int, data: LessonCreate, db: Session = Depends(get_db)):
    calendar = db.query(models.Calendar).filter(models.Calendar.id == cal_id).first()
    if calendar_id not in calendar:
        raise HTTPException(status_code = 404, detail = "Calendar not found")
    new_lesson = models.Lesson(
        name = data.name,
        room = data.room,
        day_of_week = data.day_of_week,
        time_start = data.time_start,
        time_end = data.time_end,
        descriptions = data.descriptions,
        color = data.color,
        is_reccuring = data.is_reccuring,
        links = data.links,
        files = data.files,
        calendar_id = calendar_id,
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

@app.get("/user/{cal_id}/lessons/", response_model = list[Lesson])
def list_lesson(calendar_id: int, db: Session = Depends(get_db)):
    return db.query(models.Calendar).filter(models.Lesson.Calendar.id == cal_id).all()

@app.put("/calendars/{cal_id}/lessons/{les_id}", response_model = Lesson)
def update_lesson(cal_id: int, les_id: int, data: LessonCreate, bd: Session = Depends(get_db)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == les_id).first()
    if les_id not in lessons:
        raise HTTPException(status_code = 404, detail = "Lesson not found")
    if cal_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calender not found")

    lesson.name = data.name
    lesson.room = data.room
    lesson.day_of_week = data.day_of_week
    lesson.time_start = data.time_start
    lesson.time_end = data.time_end
    lesson.descriptions = data.descriptions
    lesson.color = data.color
    lesson.is_reccuring = data.is_reccuring
    lesson.links = data.links
    lesson.files = data.files
    lesson.calendar_id = calendar_id

    db.commit()
    db.refresh(lesson)
    return lesson

@app.delete("/calendars/{cal_id}/lessons/{les_id}")
def delete_lesson(cal_id: int, les_id: int, db: Session = Depends(get_db)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == les_id).first()
    if les_id not in lessons:
        raise HTTPException(status_code = 404, detail = "Lesson not found")
    
    db.delete(lesson)
    db.commit()
    return {"message": f"Lesson {les_id} deleted"}



#Task
@app.post("/task", response_model = Task)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    if data.calendar_id not in calendar:
        raise HTTPException(status_code = 404, detail = "Calendar not found")
    new_task = models.Task(
        title = data.title,
        descriptions = data.descriptions,
        day = data.day,
        time = data.time,
        deadline = data.deadline,
        color = data.color,
        links = data.links,
        files = data.files,
        is_done = data.is_done,
        calendar_id = data.calendar_id,
        lesson_id = data.is_donelesson_id,
        parent_task_id = data.parent_task_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/calendars/{calendar_id}/tasks/", response_model = list[Task])
def list_tasks(calendar_id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.Calendar.id == calendar_id).all()

@app.patch("/tasks/{task_id}/toggle-done", response_model = Task)
def toggle_done(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code = 404, detail = "Task not found")

    task.is_done = not task.is_done
    db.commit()
    db.refresh(task)
    return task

@app.put("/tasks/{task_id}", response_model = Task)
def update_task(task_id: int, data: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task_id not in tasks:
        raise HTTPException(status_code = 404, detail = "Task not found")
    calendar = db.query(models.Calendar).filter(models.Calendar.id == data.calendar_id).first()    
    if data.calendar_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calendar not found")

    task.calendar_id = data.calendar_id
    task.lesson_id = data.lesson_id
    task.parent_task_id = data.parent_task_id
    task.title = data.title
    task.descriptions = data.descriptions
    task.day = data.day
    task.time = data.time
    task.deadline = data.deadline
    task.color = data.color 
    task.links = data.links
    task.files = data.files
    task.is_done = data.is_done

    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task_id not in tasks:
        raise HTTPException(status_code = 404, detail = "Task not found")

    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted"}


#Notes
@app.post("/notes", response_model = Note)
def create_notes(data: NoteCreate, db: Session = Depends(get_db)):
    calendar = db.query(models.Calendar).filter(models.Calendar.id == data.calendar_id).first()
    if data.calendar_id not in calendar:
        raise HTTPException(status_code = 404, detail = "Calendar not found")
    new_note = models.Note(
        calendar_id = data.calendar_id,
        day = data.day,
        text = data.text,
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/notes/{note_id}", response_model = Note)
def update_note(note_id: int, data: NoteCreate, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note_id not in notes:
        raise HTTPException(status_code = 404, detail = "Note not found")
    calendar = db.query(models.Calendar).filter(models.Calendar.id == data.calendar_id).first()
    if data.calendar_id not in calendars:
        raise HTTPException(status_code = 404, detail = "Calendar not found")

    note.calendar_id = data.calendar_id
    note.day = data.day
    note.text = data.text

    db.commit()
    db.refresh(note)
    return note

@app.delete("/notes/{note_id}")
def detele_note(note_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note_id not in notes:
        raise HTTPException(status_code = 404, detail = "Note not found")

    db.delete(note)
    db.commit()
    return {"message": f"Note {note_id} deleted"}