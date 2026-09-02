from sqlalchemy import Integer, Column, Boolean, String, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True)
    nickname = Column(String)
    password = Column(String)

    calendars = relationship("Calendar", back_populates = "owner")

class Calendar(Base):
    __tablename__ = "calendars"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    color = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates = "calendars")
    lessons = relationship("Lesson", back_populates = "calendar")
    tasks = relationship("Task", back_populates = "calendar")
    notes = relationship("Note", back_populates = "calendar")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    room = Column(String, nullable = True)
    day_of_week = Column(String)
    time_start = Column(String)
    time_end = Column(String)
    description = Column(String, nullable = True)
    color = Column(String, default = "#3498db")
    is_reccurind = Column(Boolean, default = True)
    links = Column(ARRAY(String), default = [])
    files = Column(ARRAY(String), default = [])

    calendar_id = Column(Integer, ForeignKey("calendars.id"))
    calendar = relationship("Calendar", back_populates = "lessons")

    tasks = relationship("Task", back_populates = "lesson")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String, nullable = True)
    day = Column(String)
    time = Column(String, nullable = True)
    deadline = Column(String, nullable = True)
    color = Column(String, default = "#2ecc71")
    links = Column(ARRAY(String), default = [])
    files = Column(ARRAY(String), default = [])
    is_done = Column(Boolean, default = False)

    calendar_id = Column(Integer, ForeignKey("calendars.id"))
    calendar = relationship("Calendar", back_populates = "tasks")

    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable = True)
    lesson = relationship("Lesson", back_populates = "task")

    parent_task_id = Column(Integer, ForeignKey("task.id"), nullable = True)
    subtasks = relationship("Task", back_populates = "parent_task", remote_side =[id])
    parent_task = relationship("Task", back_populates = "subtasks", remote_side = [parent_task_id])

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key = True, index = True)
    day = Column(String)
    text = Column(String)

    calendar_id = Column(Integer, ForeignKey("calendars.id"))
    calendar = relationship("Calendar", back_populates = "notes")
