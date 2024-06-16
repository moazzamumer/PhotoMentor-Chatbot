from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    chat_id = Column(Integer, primary_key=True, index=True)
    role = Column(String, index=True)
    text = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, index=True)
