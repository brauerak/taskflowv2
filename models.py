from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
import enum
from datetime import datetime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PriorityLevel(enum.Enum):
    low = 'Low'
    medium = 'Medium'
    high = 'High'

class Categories(enum.Enum):
    work = "Work"
    household = "Household"
    education = "Study & Education"
    personal = "Personal"
    health = "Fitness & Health"
    shopping = "Shopping"
    family = "Familiy & Social"
    travel = "Travel"
    projects = "Projects"
    urgent = "Urgent"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    # I added (128) to get enough space for hashed password 
    password = Column(String(128))
    firt_name = Column(String)
    last_name = Column(String)
    # datetime.utcnow allows me to automatically receive the account creation time 
    created_at = Column(DateTime, default=datetime.utcnow)
    # that means User has an atribut 'tasks', which has list if all 'Task' related with user
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    title = Column(String)
    description = Column(String, default='none')
    completed = Column(Boolean, default=False)
    priority = Column(Enum(PriorityLevel))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates='tasks')

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship("Task", back_populates='category')