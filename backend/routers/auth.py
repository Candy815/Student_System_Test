from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from database import get_db
from models import User, UserRole, Student, Teacher

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: str = "guest"

router = APIRouter()

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = "your-secret-key-here"  # 在生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    # 首先尝试bcrypt验证
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        # 如果bcrypt验证失败，尝试SHA-256验证（用于测试数据）
        import hashlib
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password):
    # Temporarily use SHA-256 due to bcrypt compatibility issues
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

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

@router.post("/login")
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

    # 获取用户详细信息
    user_info = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role.value
    }

    # 根据角色获取额外信息
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
    elif user.role == UserRole.GUEST:
        # 访客用户的基本信息已经在user_info中
        pass

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_info
    }

@router.post("/register")
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    # 检查用户是否已存在
    if get_user_by_username(db, request.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    # 验证角色
    try:
        user_role = UserRole(request.role)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid role. Must be guest, student, teacher, or admin"
        )

    # 创建用户
    hashed_password = get_password_hash(request.password)
    db_user = User(
        username=request.username,
        email=request.email,
        password_hash=hashed_password,
        full_name=request.full_name,
        role=user_role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User registered successfully", "user_id": db_user.id}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/upgrade-role")
async def upgrade_role(
    target_role: str,
    student_id: str = None,
    teacher_id: str = None,
    class_name: str = None,
    department: str = None,
    title: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 只有访客可以升级身份
    if current_user.role != UserRole.GUEST:
        raise HTTPException(
            status_code=400,
            detail="Only guest users can upgrade their role"
        )

    # 验证目标角色
    if target_role not in ["student", "teacher"]:
        raise HTTPException(
            status_code=400,
            detail="Target role must be student or teacher"
        )

    # 检查是否已经申请过升级
    if hasattr(current_user, 'upgrade_request') and current_user.upgrade_request:
        raise HTTPException(
            status_code=400,
            detail="You already have a pending upgrade request"
        )

    # 创建升级请求
    from models import UpgradeRequest
    upgrade_request = UpgradeRequest(
        user_id=current_user.id,
        target_role=target_role,
        student_id=student_id,
        teacher_id=teacher_id,
        class_name=class_name,
        department=department,
        title=title,
        status="pending"
    )

    db.add(upgrade_request)
    db.commit()

    return {"message": "Upgrade request submitted successfully", "request_id": upgrade_request.id}

@router.get("/upgrade-requests")
async def get_upgrade_requests(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 只有管理员可以查看所有升级请求
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admin can view upgrade requests"
        )

    from models import UpgradeRequest
    requests = db.query(UpgradeRequest).filter(UpgradeRequest.status == "pending").all()
    return requests

@router.post("/approve-upgrade/{request_id}")
async def approve_upgrade(
    request_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 只有管理员可以批准升级请求
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admin can approve upgrade requests"
        )

    from models import UpgradeRequest, Student, Teacher
    upgrade_request = db.query(UpgradeRequest).filter(UpgradeRequest.id == request_id).first()

    if not upgrade_request:
        raise HTTPException(
            status_code=404,
            detail="Upgrade request not found"
        )

    if upgrade_request.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Upgrade request already processed"
        )

    # 获取用户
    user = db.query(User).filter(User.id == upgrade_request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 更新用户角色
    target_role = UserRole(upgrade_request.target_role)
    user.role = target_role

    # 创建相应的档案
    if target_role == UserRole.STUDENT:
        if not upgrade_request.student_id:
            raise HTTPException(
                status_code=400,
                detail="Student ID is required for student role"
            )

        # 检查学号是否已存在
        existing_student = db.query(Student).filter(Student.student_id == upgrade_request.student_id).first()
        if existing_student:
            raise HTTPException(
                status_code=400,
                detail="Student ID already exists"
            )

        student = Student(
            user_id=user.id,
            student_id=upgrade_request.student_id,
            class_name=upgrade_request.class_name,
            enrollment_year=2024  # 默认当前年份
        )
        db.add(student)

    elif target_role == UserRole.TEACHER:
        if not upgrade_request.teacher_id:
            raise HTTPException(
                status_code=400,
                detail="Teacher ID is required for teacher role"
            )

        # 检查工号是否已存在
        existing_teacher = db.query(Teacher).filter(Teacher.teacher_id == upgrade_request.teacher_id).first()
        if existing_teacher:
            raise HTTPException(
                status_code=400,
                detail="Teacher ID already exists"
            )

        teacher = Teacher(
            user_id=user.id,
            teacher_id=upgrade_request.teacher_id,
            department=upgrade_request.department,
            title=upgrade_request.title
        )
        db.add(teacher)

    # 更新请求状态
    upgrade_request.status = "approved"
    upgrade_request.processed_at = datetime.utcnow()
    upgrade_request.processed_by = current_user.id

    db.commit()

    return {"message": "Upgrade request approved successfully"}

@router.post("/reject-upgrade/{request_id}")
async def reject_upgrade(
    request_id: int,
    rejection_reason: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 只有管理员可以拒绝升级请求
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admin can reject upgrade requests"
        )

    from models import UpgradeRequest
    upgrade_request = db.query(UpgradeRequest).filter(UpgradeRequest.id == request_id).first()

    if not upgrade_request:
        raise HTTPException(
            status_code=404,
            detail="Upgrade request not found"
        )

    if upgrade_request.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Upgrade request already processed"
        )

    # 更新请求状态
    upgrade_request.status = "rejected"
    upgrade_request.processed_at = datetime.utcnow()
    upgrade_request.processed_by = current_user.id
    upgrade_request.rejection_reason = rejection_reason

    db.commit()

    return {"message": "Upgrade request rejected successfully"}

@router.get("/my-upgrade-request")
async def get_my_upgrade_request(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 只有访客可以查看自己的升级请求
    if current_user.role != UserRole.GUEST:
        raise HTTPException(
            status_code=400,
            detail="Only guest users have upgrade requests"
        )

    from models import UpgradeRequest
    upgrade_request = db.query(UpgradeRequest).filter(
        UpgradeRequest.user_id == current_user.id
    ).order_by(UpgradeRequest.created_at.desc()).first()

    if not upgrade_request:
        return {"has_request": False}

    return {
        "has_request": True,
        "request": upgrade_request
    }