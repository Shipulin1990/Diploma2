# sqlalchemy_orm/queries.py

import time
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, update, and_
from models import (
    Base, Student, Course, Enrollment, Assignment, Submission,
    Schedule, Group, User
)

DATABASE_URI = 'postgresql+psycopg2://user:password@localhost/university_db'

def run_queries():
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    start_time = time.time()

    # 1. Выборка данных

    # Получить всех студентов, записанных на курс "Алгебра"
    algebra_course = session.query(Course).filter_by(name='Алгебра').first()
    students_in_algebra = session.query(Student).join(Enrollment).filter(
        Enrollment.course_id == algebra_course.id
    ).all()
    print(f"Студентов на курсе Алгебра: {len(students_in_algebra)}")

    # Получить расписание для группы "Группа А" на понедельник
    group_a = session.query(Group).filter_by(name='Группа А').first()
    monday_schedule = session.query(Schedule).filter(
        Schedule.group_id == group_a.id,
        Schedule.day_of_week == 'Monday'
    ).all()
    print(f"Занятий у Группы А в понедельник: {len(monday_schedule)}")

    # Получить задания, срок сдачи которых истекает в ближайшую неделю
    upcoming_assignments = session.query(Assignment).filter(
        Assignment.due_date <= datetime.now().date() + timedelta(days=7)
    ).all()
    print(f"Заданий с ближайшим сроком сдачи: {len(upcoming_assignments)}")

    # Получить средний балл студентов по курсу "Алгебра"
    average_grade = session.query(func.avg(Enrollment.grade)).filter(
        Enrollment.course_id == algebra_course.id
    ).scalar()
    print(f"Средний балл по Алгебре: {average_grade}")

    # 2. Вставка данных

    new_students = []
    for i in range(100):
        user = User(
            username=f'student_new_{i}',
            password='password123',
            email=f'student_new_{i}@example.com',
            first_name='Новый',
            last_name=f'Студент_{i}',
            role='student'
        )
        student = Student(
            user=user,
            student_number=f'SN_{i}',
            enrollment_date=datetime.now().date()
        )
        session.add(student)
        new_students.append(student)

    session.commit()

    # Записать новых студентов на курс "Алгебра"
    enrollments = [
        Enrollment(
            student_id=student.user_id,
            course_id=algebra_course.id,
            enrollment_date=datetime.now().date()
        )
        for student in new_students
    ]
    session.bulk_save_objects(enrollments)
    session.commit()
    print("Добавлено 100 новых студентов и записано на курс 'Алгебра'.")

    # 3. Обновление данных

    session.query(Enrollment).filter(
        Enrollment.course_id == algebra_course.id
    ).update(
        {Enrollment.grade: Enrollment.grade * 1.05},
        synchronize_session=False
    )
    session.commit()
    print("Оценки студентов по 'Алгебре' повышены на 5%.")

    # 4. Удаление данных

    one_year_ago = datetime.now().date() - timedelta(days=365)
    old_submissions = session.query(Submission).filter(
        Submission.submission_date <= one_year_ago
    )
    deleted_count = old_submissions.count()
    old_submissions.delete(synchronize_session=False)
    session.commit()
    print(f"Удалено {deleted_count} старых ответов на задания.")

    end_time = time.time()
    print(f"Время выполнения запросов SQLAlchemy ORM: {end_time - start_time} секунд.")

    session.close()

if __name__ == '__main__':
    run_queries()
