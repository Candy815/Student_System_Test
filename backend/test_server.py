from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="学生管理系统 API",
    description="一个完整的学生管理系统后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    print("启动测试服务器...")
    print("API文档: http://127.0.0.1:8002/docs")
    print("健康检查: http://127.0.0.1:8002/health")
    uvicorn.run(app, host="127.0.0.1", port=8002)