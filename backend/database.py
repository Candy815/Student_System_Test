from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# 强制使用SQLite数据库，避免环境变量问题
DATABASE_URL = "sqlite:///./student_system.db"

# 对于SQLite，添加必要的连接选项
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

print(f"数据库连接URL: {engine.url}")
print("连接数据库成功")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()