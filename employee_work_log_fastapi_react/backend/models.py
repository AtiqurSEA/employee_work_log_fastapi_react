from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="regular")

    work_logs = relationship("WorkLog", back_populates="user", cascade="all, delete")


class WorkLog(Base):
    __tablename__ = "work_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    task = Column(String(255), nullable=False)
    hours = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    project = Column(String(100), nullable=False)
    comments = Column(Text, nullable=True)

    user = relationship("User", back_populates="work_logs")
