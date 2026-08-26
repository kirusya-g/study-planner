from fastapi import FastAPI
from pydantic import BaseModel

#User(data that come from client)
class UselCreate(BaseModel):
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















app = FastAPI()
@app.get("/")
def root():
    return {"message": "Study Planner API"}
@app.get("/calendars")
def get_calendars():
    calendars = [
        {
           "id": 1,
            "name": "University",
            "color": "#A8D8EA" 
        },
        {
            "id": 2,
            "name": "Personal",
            "color": "#CDB4DB"
        }
    ]
    return calendars