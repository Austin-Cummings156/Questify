
# src/database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime, Date, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import enum
import os

# Define base directory and database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, '..', 'data', 'questify.db')

# Create engine (SQLite database)
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=False)

# Create base class for models
Base = declarative_base()

# Enum for status and priority
class Status(enum.Enum):
    active = "active"
    on_hold = "on_hold"
    archived = "archived"

class Priority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Frequency(enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    one_time = "one_time"

# Users table
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100))
    level = Column(Integer, nullable=False, default=1)
    current_xp = Column(Integer, nullable=False, default=0)
    xp_to_next_level = Column(Integer, nullable=False, default=100)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pursuits table
class Pursuit(Base):
    __tablename__ = 'pursuits'
    pursuit_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    xp_reward = Column(Integer, nullable=False, default=0)
    percent_completed = Column(Float, nullable=False, default=0.0)
    is_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(Date)
    status = Column(Enum(Status), nullable=False, default=Status.active)
    category = Column(String(50))

# Quests table
class Quest(Base):
    __tablename__ = 'quests'
    quest_id = Column(Integer, primary_key=True)
    pursuit_id = Column(Integer, ForeignKey('pursuits.pursuit_id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    xp_reward = Column(Integer, nullable=False, default=0)
    is_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(Date)
    priority = Column(Enum(Priority), nullable=False, default=Priority.medium)
    frequency = Column(Enum(Frequency), nullable=False, default=Frequency.one_time)

# Create tables and indexes
def init_db():
    Base.metadata.create_all(engine)
    # Create indexes
    from sqlalchemy import Index
    Index('idx_pursuits_user_id', Pursuit.user_id).create(engine)
    Index('idx_quests_pursuit_id', Quest.pursuit_id).create(engine)
    Index('idx_quests_user_id', Quest.user_id).create(engine)

# Session factory for database operations
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    init_db()
    print(f"Database initialized at {DATABASE_PATH}")