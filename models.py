from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, Text, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime

db = SQLAlchemy()

# モデルクラスの定義
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(Text(128), nullable=False)
    email = Column(String(128), nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String(128), nullable=False)
    knowlet = relationship("Knowlet", cascade="delete", backref="users")
    
    def __init__(self, username, email, age, password):
        self.username = username
        self.email = email
        self.age = age
        self.password = password
    
    def __repr__(self):
        return f'User: {self.username}'

# モデルクラスの定義
class Knowlet(db.Model):
    __tablename__ = 'knowlets'
    id = Column(Integer, primary_key = True)
    title = Column(Text(128), index = True, nullable=False)
    content = Column(Text(256), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    resolved = Column(Boolean)
    
    def __init__(self, title, content, user_id, resolved=False):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.resolved = resolved
    
    def __repr__(self):
        return f'Knowlet: {self.title}'