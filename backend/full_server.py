#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import uvicorn

# 导入我们的模块
from database import engine, get_db
from models import Base, User, UserRole, Student, Teacher, Course, Enrollment, Grade, Attendance, Exam, SystemLog, Notice

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="学生管理系统 API",
    description="一个完整的学生管理系统后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        import hashlib
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# 认证路由
@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value}
    )

    user_info = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role.value
    }

    if user.role == UserRole.STUDENT:
        student = db.query(Student).filter(Student.user_id == user.id).first()
        if student:
            user_info.update({
                "student_id": student.student_id,
                "class_name": student.class_name
            })
    elif user.role == UserRole.TEACHER:
        teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
        if teacher:
            user_info.update({
                "teacher_id": teacher.teacher_id,
                "department": teacher.department,
                "title": teacher.title
            })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_info
    }

@app.get("/auth/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# 学生仪表板路由
@app.get("/students/dashboard")
async def get_student_dashboard(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Not authorized")

    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student.id,
        Enrollment.status == "active"
    ).all()

    courses = []
    for enrollment in enrollments:
        course = enrollment.course
        courses.append({
            "id": course.id,
            "name": course.name,
            "teacher": course.teacher.user.full_name if course.teacher else "未分配",
            "time": course.schedule,
            "room": course.classroom,
            "credits": course.credits
        })

    grades = db.query(Grade).filter(Grade.student_id == student.id).all()
    grade_list = []
    for grade in grades:
        grade_list.append({
            "course": grade.course.name,
            "midterm": grade.midterm_score,
            "final": grade.final_score,
            "usual": grade.usual_score,
            "total": grade.total_score,
            "gpa": grade.gpa
        })

    total_credits = sum(course["credits"] for course in courses)
    avg_gpa = sum(grade["gpa"] for grade in grade_list) / len(grade_list) if grade_list else 0

    return {
        "student_info": {
            "name": current_user.full_name,
            "student_id": student.student_id,
            "class_name": student.class_name,
            "email": current_user.email
        },
        "courses": courses,
        "grades": grade_list,
        "stats": {
            "total_courses": len(courses),
            "total_credits": total_credits,
            "average_gpa": round(avg_gpa, 2)
        }
    }

# 基础路由
@app.get("/")
async def root():
    return {
        "message": "欢迎使用学生管理系统 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("启动学生管理系统后端服务...")
    print("API文档: http://127.0.0.1:8002/docs")
    print("健康检查: http://127.0.0.1:8002/health")
    uvicorn.run(app, host="127.0.0.1", port=8002)