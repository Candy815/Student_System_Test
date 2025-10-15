from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base
from routers import auth, students, teachers, admin, friends
from serice import ai_service

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

# 包含路由
app.include_router(auth.router, prefix="/auth", tags=["认证"])
app.include_router(students.router, prefix="/students", tags=["学生"])
app.include_router(teachers.router, prefix="/teachers", tags=["教师"])
app.include_router(admin.router, prefix="/admin", tags=["管理员"])
app.include_router(friends.router, prefix="/friends", tags=["好友"])
app.include_router(ai_service.router, prefix="/ai", tags=["AI助手"])

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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)