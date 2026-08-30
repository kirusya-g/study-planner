from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    links = List[str] = []
    files = List[str] = []

class Lesson(LessonCreate):
    id: int

#Task
class TaskCreate(BaseModel):
    calendar_id: int
    lesson_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    title: str
    descriprions: Oprional[str] = None
    day: str
    time: Optional[str] = None
    deadline: Optional[str] = None
    color:  str = "#2ecc71"
    links = List[str] = []
    files = List[str] = []
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
    users[user_id] = user
    return user

@app.get("/user/{user_id}", response_model = User)
def get_user(user_id: int):
    user = user.get(user_id)
    if not user:
        raise HTTPException(status_code = 404, details = "User not found")
    return user

#Calendar
@app.post("/users/{user_id}/calendars/", response_model = Calendar)
def create_calendar(user_id: int, data: CalendarCreate):
    if user_id not in user:
        raise HTTPException(status_code = 404, details = "User not found")
    cal_id = next_id("calendar")
    calendar = {"id": cal_id, "user_id": user_id, **data.model_dump()}
    calendars[cal_id] = calendar
    return calendar

@app.get("/user/{user_id}/calendars/", response_model = list[Calendar])
def list_calendar(user_id: int):
    return [c for c in calendar.values() if c["user_id"] == user_id]

#Lesson
@app.post("/calendars/{calendar_id}/lessons/", response_model = Lesson)
def create_lesson(calendar_id: int, data: LessonCreate):
    if calendar_id not in calendar:
        raise HTTPException(status_code = 404, details = "Calendar not found")
    les_id = next_id("lesson")
    lesson = {"id": les_id, **data.model_dump()}
    lessons[les_id] = lesson
    return lesson

@app.get("/user/{calender_id}/lessons/", response_model = list[Lesson])
def list_lesson(user_id: int):
    return [l for l in lesson.values() if l["calendar_id"] == calendar_id]

#Task
@app.post("/task", resposne_model = Lesson)
def create_task(data: TaskCreate):
    if calendar_id not in calendar:
        raise HTTPException(status_code = 404, details = "Calendar not found")
    task_id = next_id("task")
    task = {"id": task_id, **data.model_dump()}
    tasks[task_id] = task
    return task

@app.get("/calendars/{calendar_id}/tasks/", response_model = lisr[Task])
def list_calendar(calendar_id: int):
    return [t for t in task.values() if l["calendar_id"] == calendar_id]

@app.patch("/tasks/{task_id}/toggle-done", response_model = Task)
def toggle_done(task_id: int):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code = 404, details = "Task not found")
    task["is_done"] = not task["is_done"]
    return task

#Notes
@app.post("/notes", response_model = Notes)
def create_notes(notes: NoteCreate):
    if data.calendar_id not in calendar:
        raise HTTPException(status_code = 404, details = "Calendar not found")
    note_id = next_id("note")
    note = {"id": note_id, **data.model_dump()}
    notes[note_id] = note
    return note