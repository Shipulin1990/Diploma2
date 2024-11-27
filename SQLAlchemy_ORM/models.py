from sqlalchemy import (
    Column, String, Integer, Date, DateTime, ForeignKey, Table, Time, Enum, UniqueConstraint
)
from sqlalchemy.orm import relationship
from database import Base
import enum

# Определение перечислений
class UserRole(enum.Enum):
    student = 'student'
    teacher = 'teacher'
    administrator = 'administrator'

class MaterialType(enum.Enum):
    lecture = 'lecture'
    presentation = 'presentation'
    document = 'document'

class DayOfWeek(enum.Enum):
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    Sunday = 'Sunday'

# 1. Пользователи
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    role = Column(Enum(UserRole), nullable=False)

    # Отношения
    student = relationship('Student', back_populates='user', uselist=False)
    teacher = relationship('Teacher', back_populates='user', uselist=False)

# 2. Студенты
class Student(Base):
    __tablename__ = 'students'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    student_number = Column(String(20), unique=True, nullable=False)
    enrollment_date = Column(Date, nullable=False)

    # Отношения
    user = relationship('User', back_populates='student')
    enrollments = relationship('Enrollment', back_populates='student')
    submissions = relationship('Submission', back_populates='student')
    groups = relationship('Group', secondary='student_groups', back_populates='students')

# 3. Преподаватели
class Teacher(Base):
    __tablename__ = 'teachers'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    employee_number = Column(String(20), unique=True, nullable=False)
    hire_date = Column(Date, nullable=False)
    department = Column(String(100))

    # Отношения
    user = relationship('User', back_populates='teacher')
    courses = relationship('TeacherCourse', back_populates='teacher')
    schedules = relationship('Schedule', back_populates='teacher')

# 4. Курсы
class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String)
    credits = Column(Integer, nullable=False)

    # Отношения
    assignments = relationship('Assignment', back_populates='course')
    materials = relationship('CourseMaterial', back_populates='course')
    enrollments = relationship('Enrollment', back_populates='course')
    teachers = relationship('TeacherCourse', back_populates='course')
    schedules = relationship('Schedule', back_populates='course')

# 5. Группы
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)

    # Отношения
    students = relationship('Student', secondary='student_groups', back_populates='groups')
    schedules = relationship('Schedule', back_populates='group')

# 6. Записи студентов в группы (многие-ко-многим)
student_groups = Table(
    'student_groups',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.user_id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)

# 7. Преподаватели и Курсы (многие-ко-многим)
class TeacherCourse(Base):
    __tablename__ = 'teacher_courses'
    teacher_id = Column(Integer, ForeignKey('teachers.user_id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)

    # Отношения
    teacher = relationship('Teacher', back_populates='courses')
    course = relationship('Course', back_populates='teachers')

# 8. Записи студентов на курсы
class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.user_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    grade = Column(Integer)

    # Уникальность записи
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='uix_student_course'),
    )

    # Отношения
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')

# 9. Задания
class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String)
    due_date = Column(Date, nullable=False)

    # Отношения
    course = relationship('Course', back_populates='assignments')
    submissions = relationship('Submission', back_populates='assignment')

# 10. Ответы на задания
class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.user_id'), nullable=False)
    submission_date = Column(Date, nullable=False)
    file_path = Column(String)
    grade = Column(Integer)

    # Уникальность записи
    __table_args__ = (
        UniqueConstraint('assignment_id', 'student_id', name='uix_assignment_student'),
    )

    # Отношения
    assignment = relationship('Assignment', back_populates='submissions')
    student = relationship('Student', back_populates='submissions')

# 11. Материалы курса
class CourseMaterial(Base):
    __tablename__ = 'course_materials'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(200), nullable=False)
    material_type = Column(Enum(MaterialType), nullable=False)
    file_path = Column(String)

    # Отношения
    course = relationship('Course', back_populates='materials')

# 12. Расписание
class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.user_id'), nullable=False)
    classroom = Column(String(50))
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)

    # Отношения
    course = relationship('Course', back_populates='schedules')
    group = relationship('Group', back_populates='schedules')
    teacher = relationship('Teacher', back_populates='schedules')

