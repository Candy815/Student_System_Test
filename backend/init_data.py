from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, UserRole, Student, Teacher, Course, Enrollment, Grade, Notice
import hashlib

def simple_hash(password):
    """简单的密码哈希函数，用于测试"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_test_data():
    # 导入并创建数据库表
    from models import Base
    from database import engine
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # 创建管理员用户
        admin_user = User(
            username="admin",
            email="admin@system.com",
            password_hash=simple_hash("admin123"),
            full_name="系统管理员",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        # 创建教师用户
        teacher_user = User(
            username="teacher001",
            email="teacher@university.edu.cn",
            password_hash=simple_hash("teacher123"),
            full_name="李老师",
            role=UserRole.TEACHER,
            is_active=True
        )
        db.add(teacher_user)
        db.commit()
        db.refresh(teacher_user)

        # 创建教师档案
        teacher = Teacher(
            user_id=teacher_user.id,
            teacher_id="T001",
            department="计算机科学系",
            title="副教授",
            phone="13800138000",
            office_address="计算机楼A301"
        )
        db.add(teacher)
        db.commit()
        db.refresh(teacher)

        # 创建学生用户
        student_user = User(
            username="2023001",
            email="zhangsan@student.edu.cn",
            password_hash=simple_hash("student123"),
            full_name="张三",
            role=UserRole.STUDENT,
            is_active=True
        )
        db.add(student_user)
        db.commit()
        db.refresh(student_user)

        # 创建学生档案
        student = Student(
            user_id=student_user.id,
            student_id="2023001",
            class_name="计算机科学2023-1班",
            enrollment_year=2023,
            phone="13900139000",
            address="学生宿舍1号楼101室"
        )
        db.add(student)
        db.commit()
        db.refresh(student)

        # 创建课程
        courses = [
            {
                "name": "数据结构与算法",
                "code": "CS201",
                "description": "计算机科学核心课程",
                "credits": 4,
                "teacher_id": teacher.id,
                "classroom": "A101",
                "schedule": "周一、三 8:00-9:30",
                "max_students": 50
            },
            {
                "name": "计算机网络",
                "code": "CS301",
                "description": "网络原理与应用",
                "credits": 3,
                "teacher_id": teacher.id,
                "classroom": "B203",
                "schedule": "周二、四 10:00-11:30",
                "max_students": 40
            },
            {
                "name": "操作系统原理",
                "code": "CS401",
                "description": "操作系统设计与实现",
                "credits": 4,
                "teacher_id": teacher.id,
                "classroom": "C305",
                "schedule": "周一、五 14:00-15:30",
                "max_students": 45
            }
        ]

        for course_data in courses:
            course = Course(**course_data)
            db.add(course)
            db.commit()
            db.refresh(course)

            # 学生选课
            enrollment = Enrollment(
                student_id=student.id,
                course_id=course.id,
                status="active"
            )
            db.add(enrollment)

            # 添加一些成绩
            grade = Grade(
                student_id=student.id,
                course_id=course.id,
                midterm_score=85.0 if course.name == "数据结构与算法" else 82.0,
                final_score=88.0 if course.name == "数据结构与算法" else 86.0,
                usual_score=90.0 if course.name == "数据结构与算法" else 88.0,
                total_score=87.4 if course.name == "数据结构与算法" else 85.2,
                gpa=3.7 if course.name == "数据结构与算法" else 3.5,
                semester="2024-1",
                academic_year="2024",
                status="approved"
            )
            db.add(grade)

        # 创建系统通知
        notices = [
            {
                "title": "关于期末考试安排的通知",
                "content": "期末考试将于第16周开始，请各位同学做好准备。",
                "priority": "high",
                "target_audience": "students",
                "author_id": admin_user.id
            },
            {
                "title": "教师培训通知",
                "content": "新教师培训将于下周三在会议室举行。",
                "priority": "normal",
                "target_audience": "teachers",
                "author_id": admin_user.id
            },
            {
                "title": "系统维护通知",
                "content": "系统将于本周六凌晨2-4点进行维护。",
                "priority": "urgent",
                "target_audience": "all",
                "author_id": admin_user.id
            }
        ]

        for notice_data in notices:
            notice = Notice(**notice_data)
            db.add(notice)

        db.commit()
        print("测试数据创建成功！")
        print("管理员账号: admin / admin123")
        print("教师账号: teacher001 / teacher123")
        print("学生账号: 2023001 / student123")

    except Exception as e:
        print(f"创建测试数据失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()