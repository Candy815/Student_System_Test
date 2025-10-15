from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from database import get_db
from models import User, UserRole, Student, Course, Enrollment, Grade, Attendance, Exam
# 将在函数内导入以避免循环导入

router = APIRouter()

def get_student_user(current_user):
    from routers.auth import get_current_active_user, get_db
    current_user = get_current_active_user(current_user)
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access student resources"
        )
    return current_user

@router.get("/dashboard")
async def get_student_dashboard(
    current_user: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    # 获取学生信息
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    # 获取学生课程
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

    # 获取学生成绩
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

    # 获取即将到来的考试
    exams = db.query(Exam).join(Course).join(Enrollment).filter(
        Enrollment.student_id == student.id,
        Exam.date > datetime.now()
    ).all()

    upcoming_exams = []
    for exam in exams:
        upcoming_exams.append({
            "course": exam.course.name,
            "date": exam.date.strftime("%Y-%m-%d"),
            "time": f"{exam.date.strftime('%H:%M')}-{(exam.date + timedelta(minutes=exam.duration)).strftime('%H:%M')}",
            "room": exam.location
        })

    # 计算统计数据
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
        "upcoming_exams": upcoming_exams,
        "stats": {
            "total_courses": len(courses),
            "total_credits": total_credits,
            "average_gpa": round(avg_gpa, 2)
        }
    }

@router.get("/courses")
async def get_student_courses(
    current_user: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
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
            "code": course.code,
            "teacher": course.teacher.user.full_name if course.teacher else "未分配",
            "schedule": course.schedule,
            "classroom": course.classroom,
            "credits": course.credits,
            "description": course.description,
            "enrollment_date": enrollment.enrollment_date.isoformat()
        })

    return courses

@router.get("/grades")
async def get_student_grades(
    current_user: User = Depends(get_student_user),
    semester: Optional[str] = None,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    query = db.query(Grade).filter(Grade.student_id == student.id)
    if semester:
        query = query.filter(Grade.semester == semester)

    grades = query.all()
    grade_list = []
    for grade in grades:
        grade_list.append({
            "id": grade.id,
            "course": grade.course.name,
            "course_code": grade.course.code,
            "midterm_score": grade.midterm_score,
            "final_score": grade.final_score,
            "usual_score": grade.usual_score,
            "total_score": grade.total_score,
            "gpa": grade.gpa,
            "semester": grade.semester,
            "academic_year": grade.academic_year,
            "graded_at": grade.graded_at.isoformat(),
            "status": grade.status
        })

    return grade_list

@router.get("/schedule")
async def get_student_schedule(
    current_user: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student.id,
        Enrollment.status == "active"
    ).all()

    schedule = []
    for enrollment in enrollments:
        course = enrollment.course
        if course.schedule:
            schedule.append({
                "course_id": course.id,
                "course_name": course.name,
                "teacher": course.teacher.user.full_name if course.teacher else "未分配",
                "schedule": course.schedule,
                "classroom": course.classroom,
                "credits": course.credits
            })

    return schedule

@router.get("/exams")
async def get_student_exams(
    current_user: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    exams = db.query(Exam).join(Course).join(Enrollment).filter(
        Enrollment.student_id == student.id
    ).all()

    exam_list = []
    for exam in exams:
        exam_list.append({
            "id": exam.id,
            "course": exam.course.name,
            "title": exam.title,
            "exam_type": exam.exam_type,
            "date": exam.date.isoformat(),
            "duration": exam.duration,
            "location": exam.location,
            "max_score": exam.max_score,
            "description": exam.description
        })

    return exam_list

@router.get("/profile")
async def get_student_profile(
    current_user: User = Depends(get_student_user),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    return {
        "id": student.id,
        "student_id": student.student_id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "class_name": student.class_name,
        "enrollment_year": student.enrollment_year,
        "phone": student.phone,
        "address": student.address
    }