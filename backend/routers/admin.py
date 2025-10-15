from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models import User, UserRole, Student, Teacher, Course, SystemLog, Notice
# 将在函数内导入以避免循环导入

router = APIRouter()

def get_admin_user(current_user):
    from routers.auth import get_current_active_user, get_db
    current_user = get_current_active_user(current_user)
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin resources"
        )
    return current_user

@router.get("/dashboard")
async def get_admin_dashboard(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    # 获取系统统计数据
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()

    total_students = db.query(Student).count()
    total_teachers = db.query(Teacher).count()
    total_courses = db.query(Course).filter(Course.is_active == True).count()
    total_departments = db.query(Teacher.department).distinct().count()

    # 获取最近活动日志
    recent_activities = db.query(SystemLog).order_by(
        SystemLog.created_at.desc()
    ).limit(10).all()

    activities = []
    for activity in recent_activities:
        user = db.query(User).filter(User.id == activity.user_id).first()
        activities.append({
            "id": activity.id,
            "user": user.full_name if user else "系统",
            "action": activity.action,
            "time": activity.created_at.strftime("%Y-%m-%d %H:%M"),
            "role": user.role.value if user else "系统",
            "status": activity.status
        })

    # 获取用户增长趋势（最近6个月）
    six_months_ago = datetime.now() - timedelta(days=180)

    student_growth = db.query(
        func.strftime('%Y-%m', User.created_at).label('month'),
        func.count(Student.id).label('count')
    ).join(User).filter(
        User.created_at >= six_months_ago,
        User.role == UserRole.STUDENT
    ).group_by('month').all()

    teacher_growth = db.query(
        func.strftime('%Y-%m', User.created_at).label('month'),
        func.count(Teacher.id).label('count')
    ).join(User).filter(
        User.created_at >= six_months_ago,
        User.role == UserRole.TEACHER
    ).group_by('month').all()

    # 组织增长数据
    user_growth_data = []
    months = []
    for i in range(6):
        month_date = datetime.now() - timedelta(days=30 * i)
        month_str = month_date.strftime('%Y-%m')
        months.insert(0, month_str)

    for month in months:
        student_count = next((s.count for s in student_growth if s.month == month), 0)
        teacher_count = next((t.count for t in teacher_growth if t.month == month), 0)
        user_growth_data.append({
            "month": month,
            "students": student_count,
            "teachers": teacher_count
        })

    # 获取系统状态（模拟）
    system_status = [
        {"service": "用户服务", "status": "正常", "uptime": "99.9%", "response": "12ms"},
        {"service": "数据库服务", "status": "正常", "uptime": "99.8%", "response": "8ms"},
        {"service": "文件服务", "status": "正常", "uptime": "99.7%", "response": "45ms"},
        {"service": "邮件服务", "status": "警告", "uptime": "98.5%", "response": "120ms"},
        {"service": "缓存服务", "status": "正常", "uptime": "99.9%", "response": "2ms"}
    ]

    # 获取安全警告（模拟）
    security_alerts = [
        {"id": 1, "type": "high", "title": "检测到异常登录尝试", "count": 5, "time": "最近1小时"},
        {"id": 2, "type": "medium", "title": "用户密码重置异常", "count": 3, "time": "最近24小时"},
        {"id": 3, "type": "low", "title": "系统性能警告", "count": 1, "time": "最近12小时"}
    ]

    # 获取系统通知
    notices = db.query(Notice).filter(
        Notice.is_active == True
    ).order_by(Notice.created_at.desc()).limit(5).all()

    notice_list = []
    for notice in notices:
        notice_list.append({
            "id": notice.id,
            "title": notice.title,
            "date": notice.created_at.strftime("%Y-%m-%d"),
            "urgent": notice.priority == 'urgent'
        })

    # 计算统计数据
    active_rate = (active_users / total_users * 100) if total_users > 0 else 0

    # 计算新增用户
    last_month_students = next((s.count for s in student_growth if s.month == months[-2]), 0)
    last_month_teachers = next((t.count for t in teacher_growth if t.month == months[-2]), 0)

    critical_alerts = len([alert for alert in security_alerts if alert['type'] == 'high'])
    normal_services = len([service for service in system_status if service['status'] == '正常'])

    return {
        "system_stats": {
            "total_users": total_users,
            "active_users": active_users,
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_courses": total_courses,
            "total_departments": total_departments
        },
        "recent_activities": activities,
        "user_growth_data": user_growth_data,
        "system_status": system_status,
        "security_alerts": security_alerts,
        "notices": notice_list,
        "calculated_stats": {
            "active_rate": round(active_rate, 1),
            "recent_new_students": last_month_students,
            "recent_new_teachers": last_month_teachers,
            "critical_alerts": critical_alerts,
            "normal_services": normal_services
        }
    }

@router.get("/users")
async def get_users(
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if role:
        try:
            user_role = UserRole(role)
            query = query.filter(User.role == user_role)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid role")

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()

    user_list = []
    for user in users:
        user_info = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        }

        # 添加角色特定信息
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

        user_list.append(user_info)

    return {
        "users": user_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

@router.post("/users/{user_id}/toggle-status")
async def toggle_user_status(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Cannot change admin status")

    user.is_active = not user.is_active
    db.commit()

    # 记录日志
    log_entry = SystemLog(
        user_id=current_user.id,
        action=f"{'激活' if user.is_active else '禁用'}用户 {user.username}",
        resource_type="user",
        resource_id=str(user_id),
        status="success"
    )
    db.add(log_entry)
    db.commit()

    return {"message": f"User {'activated' if user.is_active else 'deactivated'} successfully"}

@router.get("/courses")
async def get_all_courses(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    total = db.query(Course).count()
    courses = db.query(Course).offset((page - 1) * page_size).limit(page_size).all()

    course_list = []
    for course in courses:
        teacher_name = course.teacher.user.full_name if course.teacher else "未分配"
        enrollment_count = db.query(Enrollment).filter(
            Enrollment.course_id == course.id,
            Enrollment.status == "active"
        ).count()

        course_list.append({
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "teacher": teacher_name,
            "credits": course.credits,
            "classroom": course.classroom,
            "schedule": course.schedule,
            "enrolled_students": enrollment_count,
            "max_students": course.max_students,
            "is_active": course.is_active,
            "created_at": course.created_at.isoformat()
        })

    return {
        "courses": course_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

@router.put("/courses/{course_id}")
async def update_course(
    course_id: int,
    name: str = None,
    code: str = None,
    credits: int = None,
    teacher_id: int = None,
    classroom: str = None,
    schedule: str = None,
    max_students: int = None,
    description: str = None,
    is_active: bool = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 更新课程信息
    update_data = {}
    if name is not None:
        # 检查课程名称是否已存在
        existing_course = db.query(Course).filter(
            Course.name == name,
            Course.id != course_id
        ).first()
        if existing_course:
            raise HTTPException(status_code=400, detail="Course name already exists")
        update_data["name"] = name

    if code is not None:
        # 检查课程代码是否已存在
        existing_course = db.query(Course).filter(
            Course.code == code,
            Course.id != course_id
        ).first()
        if existing_course:
            raise HTTPException(status_code=400, detail="Course code already exists")
        update_data["code"] = code

    if credits is not None:
        if credits < 1 or credits > 10:
            raise HTTPException(status_code=400, detail="Credits must be between 1 and 10")
        update_data["credits"] = credits

    if teacher_id is not None:
        # 检查教师是否存在
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=400, detail="Teacher not found")
        update_data["teacher_id"] = teacher_id

    if classroom is not None:
        update_data["classroom"] = classroom

    if schedule is not None:
        update_data["schedule"] = schedule

    if max_students is not None:
        if max_students < 1 or max_students > 500:
            raise HTTPException(status_code=400, detail="Max students must be between 1 and 500")

        # 检查当前选课人数是否超过新的最大人数
        current_enrollments = db.query(Enrollment).filter(
            Enrollment.course_id == course_id,
            Enrollment.status == "active"
        ).count()

        if max_students < current_enrollments:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot reduce max students below current enrollment count ({current_enrollments})"
            )

        update_data["max_students"] = max_students

    if description is not None:
        update_data["description"] = description

    if is_active is not None:
        update_data["is_active"] = is_active

    # 更新课程
    for key, value in update_data.items():
        setattr(course, key, value)

    course.updated_at = datetime.utcnow()
    db.commit()

    # 记录日志
    log_entry = SystemLog(
        user_id=current_user.id,
        action=f"更新课程信息: {course.name}",
        resource_type="course",
        resource_id=str(course_id),
        status="success"
    )
    db.add(log_entry)
    db.commit()

    return {"message": "Course updated successfully"}

@router.post("/courses/{course_id}/toggle-status")
async def toggle_course_status(
    course_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    course.is_active = not course.is_active
    course.updated_at = datetime.utcnow()
    db.commit()

    # 记录日志
    log_entry = SystemLog(
        user_id=current_user.id,
        action=f"{'启用' if course.is_active else '停用'}课程: {course.name}",
        resource_type="course",
        resource_id=str(course_id),
        status="success"
    )
    db.add(log_entry)
    db.commit()

    return {"message": f"Course {'activated' if course.is_active else 'deactivated'} successfully"}

@router.post("/notices")
async def create_notice(
    title: str,
    content: str,
    priority: str = "normal",
    target_audience: str = "all",
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    notice = Notice(
        title=title,
        content=content,
        priority=priority,
        target_audience=target_audience,
        author_id=current_user.id
    )
    db.add(notice)
    db.commit()

    return {"message": "Notice created successfully", "notice_id": notice.id}

@router.get("/logs")
async def get_system_logs(
    page: int = 1,
    page_size: int = 50,
    action: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    query = db.query(SystemLog)

    if action:
        query = query.filter(SystemLog.action.contains(action))
    if status:
        query = query.filter(SystemLog.status == status)
    if start_date:
        query = query.filter(SystemLog.created_at >= start_date)
    if end_date:
        query = query.filter(SystemLog.created_at <= end_date)

    total = query.count()
    logs = query.order_by(SystemLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    log_list = []
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        log_list.append({
            "id": log.id,
            "user": user.full_name if user else "系统",
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "ip_address": log.ip_address,
            "status": log.status,
            "details": log.details,
            "created_at": log.created_at.isoformat()
        })

    return {
        "logs": log_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }