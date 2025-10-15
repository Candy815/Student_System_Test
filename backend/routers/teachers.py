from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models import User, UserRole, Teacher, Course, Enrollment, Grade, Attendance, Student
# 将在函数内导入以避免循环导入

router = APIRouter()

def get_teacher_user(current_user):
    from routers.auth import get_current_active_user, get_db
    current_user = get_current_active_user(current_user)
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access teacher resources"
        )
    return current_user

@router.get("/dashboard")
async def get_teacher_dashboard(
    current_user: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    # 获取教师信息
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    # 获取教师课程
    courses = db.query(Course).filter(Course.teacher_id == teacher.id).all()

    course_list = []
    total_students = 0
    for course in courses:
        enrollment_count = db.query(Enrollment).filter(
            Enrollment.course_id == course.id,
            Enrollment.status == "active"
        ).count()
        total_students += enrollment_count

        course_list.append({
            "id": course.id,
            "name": course.name,
            "class": f"{course.name}班级",  # 简化处理
            "students": enrollment_count,
            "time": course.schedule,
            "room": course.classroom,
            "credits": course.credits
        })

    # 获取最近录入的成绩
    recent_grades = db.query(Grade).join(Course).filter(
        Course.teacher_id == teacher.id
    ).order_by(Grade.graded_at.desc()).limit(10).all()

    grade_list = []
    for grade in recent_grades:
        student = grade.student
        grade_list.append({
            "student": student.user.full_name,
            "course": grade.course.name,
            "score": grade.total_score,
            "date": grade.graded_at.strftime("%Y-%m-%d"),
            "status": grade.status
        })

    # 获取今日课程
    today = datetime.now().strftime("%A")
    today_courses = []
    for course in courses:
        if course.schedule and today in course.schedule:
            today_courses.append({
                "course": course.name,
                "time": course.schedule,
                "room": course.classroom,
                "class": f"{course.name}班级"
            })

    # 获取学生出勤情况
    attendance_stats = []
    for course in courses:
        # 获取该课程的学生出勤统计
        stats = db.query(
            Student.user_id,
            User.full_name,
            func.count(Attendance.id).label('total'),
            func.sum(func.case([(Attendance.status == 'present', 1)], else_=0)).label('present'),
            func.sum(func.case([(Attendance.status == 'absent', 1)], else_=0)).label('absent')
        ).join(Attendance).join(User).filter(
            Attendance.course_id == course.id
        ).group_by(Student.user_id, User.full_name).all()

        for stat in stats:
            if stat.total > 0:
                attendance_rate = (stat.present / stat.total) * 100
                attendance_stats.append({
                    "student": stat.full_name,
                    "total": stat.total,
                    "present": stat.present,
                    "absent": stat.absent,
                    "rate": round(attendance_rate, 1)
                })

        # 只取前几个学生作为示例
        if len(attendance_stats) >= 4:
            break

    # 获取系统通知
    from models import Notice
    notices = db.query(Notice).filter(
        Notice.target_audience.in_(['all', 'teachers']),
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
    pending_grades = db.query(Grade).join(Course).filter(
        Course.teacher_id == teacher.id,
        Grade.status == 'draft'
    ).count()

    avg_attendance = sum(stat['rate'] for stat in attendance_stats) / len(attendance_stats) if attendance_stats else 0

    return {
        "teacher_info": {
            "name": current_user.full_name,
            "teacher_id": teacher.teacher_id,
            "department": teacher.department,
            "title": teacher.title,
            "email": current_user.email
        },
        "courses": course_list,
        "recent_grades": grade_list,
        "today_schedule": today_courses,
        "student_attendance": attendance_stats,
        "notices": notice_list,
        "stats": {
            "total_courses": len(courses),
            "total_students": total_students,
            "average_attendance": round(avg_attendance, 1),
            "pending_grades": pending_grades,
            "today_classes": len(today_courses)
        }
    }

@router.get("/courses")
async def get_teacher_courses(
    current_user: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    courses = db.query(Course).filter(Course.teacher_id == teacher.id).all()

    course_list = []
    for course in courses:
        enrollment_count = db.query(Enrollment).filter(
            Enrollment.course_id == course.id,
            Enrollment.status == "active"
        ).count()

        course_list.append({
            "id": course.id,
            "name": course.name,
            "code": course.code,
            "description": course.description,
            "credits": course.credits,
            "schedule": course.schedule,
            "classroom": course.classroom,
            "max_students": course.max_students,
            "enrolled_students": enrollment_count,
            "is_active": course.is_active,
            "created_at": course.created_at.isoformat()
        })

    return course_list

@router.get("/courses/{course_id}/students")
async def get_course_students(
    course_id: int,
    current_user: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    # 验证课程属于该教师
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.teacher_id == teacher.id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not authorized")

    # 获取选课学生
    enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.status == "active"
    ).all()

    students = []
    for enrollment in enrollments:
        student = enrollment.student
        students.append({
            "id": student.id,
            "student_id": student.student_id,
            "name": student.user.full_name,
            "email": student.user.email,
            "class_name": student.class_name,
            "enrollment_date": enrollment.enrollment_date.isoformat()
        })

    return students

@router.post("/grades")
async def submit_grade(
    student_id: int,
    course_id: int,
    midterm_score: Optional[float] = None,
    final_score: Optional[float] = None,
    usual_score: Optional[float] = None,
    semester: str = "2024-1",
    current_user: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    # 验证课程属于该教师
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.teacher_id == teacher.id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not authorized")

    # 验证学生是否选了这门课
    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id,
        Enrollment.status == "active"
    ).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Student not enrolled in this course")

    # 计算总分和GPA
    total_score = 0
    if midterm_score is not None:
        total_score += midterm_score * 0.3
    if final_score is not None:
        total_score += final_score * 0.5
    if usual_score is not None:
        total_score += usual_score * 0.2

    # 计算GPA
    if total_score >= 90:
        gpa = 4.0
    elif total_score >= 85:
        gpa = 3.7
    elif total_score >= 82:
        gpa = 3.3
    elif total_score >= 78:
        gpa = 3.0
    elif total_score >= 75:
        gpa = 2.7
    elif total_score >= 72:
        gpa = 2.3
    elif total_score >= 68:
        gpa = 2.0
    elif total_score >= 64:
        gpa = 1.5
    elif total_score >= 60:
        gpa = 1.0
    else:
        gpa = 0.0

    # 检查是否已有成绩记录
    existing_grade = db.query(Grade).filter(
        Grade.student_id == student_id,
        Grade.course_id == course_id,
        Grade.semester == semester
    ).first()

    if existing_grade:
        # 更新现有成绩
        if midterm_score is not None:
            existing_grade.midterm_score = midterm_score
        if final_score is not None:
            existing_grade.final_score = final_score
        if usual_score is not None:
            existing_grade.usual_score = usual_score
        existing_grade.total_score = total_score
        existing_grade.gpa = gpa
        existing_grade.graded_at = datetime.now()
        existing_grade.status = "submitted"
    else:
        # 创建新成绩记录
        new_grade = Grade(
            student_id=student_id,
            course_id=course_id,
            midterm_score=midterm_score,
            final_score=final_score,
            usual_score=usual_score,
            total_score=total_score,
            gpa=gpa,
            semester=semester,
            academic_year="2024",
            status="submitted"
        )
        db.add(new_grade)

    db.commit()

    return {"message": "Grade submitted successfully", "total_score": total_score, "gpa": gpa}

@router.get("/attendance/{course_id}")
async def get_course_attendance(
    course_id: int,
    current_user: User = Depends(get_teacher_user),
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher profile not found")

    # 验证课程属于该教师
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.teacher_id == teacher.id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not authorized")

    # 获取出勤记录
    attendances = db.query(Attendance).filter(Attendance.course_id == course_id).all()

    attendance_list = []
    for attendance in attendances:
        attendance_list.append({
            "id": attendance.id,
            "student": attendance.student.user.full_name,
            "student_id": attendance.student.student_id,
            "date": attendance.date.isoformat(),
            "status": attendance.status,
            "notes": attendance.notes
        })

    return attendance_list