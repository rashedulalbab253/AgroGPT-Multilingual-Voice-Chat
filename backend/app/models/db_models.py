from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
import datetime

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    language = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("chat_sessions.session_id"))
    role = Column(String) # user or assistant
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
