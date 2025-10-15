from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    GUEST = "guest"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    student_profile = relationship("Student", back_populates="user", uselist=False)
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    student_id = Column(String(20), unique=True, nullable=False)
    class_name = Column(String(100))
    enrollment_year = Column(Integer)
    phone = Column(String(20))
    address = Column(Text)

    user = relationship("User", back_populates="student_profile")
    enrollments = relationship("Enrollment", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    teacher_id = Column(String(20), unique=True, nullable=False)
    department = Column(String(100))
    title = Column(String(50))
    phone = Column(String(20))
    office_address = Column(Text)

    user = relationship("User", back_populates="teacher_profile")
    courses = relationship("Course", back_populates="teacher")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    credits = Column(Integer, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    classroom = Column(String(50))
    schedule = Column(String(200))
    max_students = Column(Integer, default=50)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teacher = relationship("Teacher", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    grades = relationship("Grade", back_populates="course")
    attendances = relationship("Attendance", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="active")  # active, dropped, completed

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    midterm_score = Column(Float)
    final_score = Column(Float)
    usual_score = Column(Float)
    total_score = Column(Float)
    gpa = Column(Float)
    semester = Column(String(20))
    academic_year = Column(String(10))
    graded_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="draft")  # draft, submitted, approved

    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")

class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    date = Column(DateTime, nullable=False)
    status = Column(String(20), default="present")  # present, absent, late, excused
    notes = Column(Text)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="attendances")
    course = relationship("Course", back_populates="attendances")

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String(100), nullable=False)
    exam_type = Column(String(20), nullable=False)  # midterm, final, quiz
    date = Column(DateTime, nullable=False)
    duration = Column(Integer)  # minutes
    location = Column(String(100))
    max_score = Column(Float, default=100)
    description = Column(Text)

    course = relationship("Course")

class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    target_audience = Column(String(50))  # all, students, teachers, admin
    author_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("User")

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(50))
    ip_address = Column(String(45))
    status = Column(String(20), default="success")  # success, failed, warning
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class UpgradeRequest(Base):
    __tablename__ = "upgrade_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target_role = Column(String(20), nullable=False)  # student, teacher
    student_id = Column(String(20))
    teacher_id = Column(String(20))
    class_name = Column(String(100))
    department = Column(String(100))
    title = Column(String(50))
    status = Column(String(20), default="pending")  # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    processed_by = Column(Integer, ForeignKey("users.id"))
    rejection_reason = Column(Text)

    user = relationship("User", foreign_keys=[user_id])
    processor = relationship("User", foreign_keys=[processed_by])

class FriendRequest(Base):
    __tablename__ = "friend_requests"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending, accepted, rejected
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="active")  # active, blocked

    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])