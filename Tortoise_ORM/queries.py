# tortoise_orm/queries.py

import asyncio
import time
from datetime import date, timedelta
from tortoise import Tortoise, run_async, transactions
from models import (
    Student, Course, Enrollment, Assignment, Submission,
    Schedule, Group, User
)

async def run_queries():
    await Tortoise.init(
        db_url='postgres://user:password@localhost:5432/university_db',
        modules={'models': ['models']}
    )
    start_time = time.time()

    # 1. Выборка данных

    # Получить всех студентов, записанных на курс "Алгебра"
    algebra_course = await Course.get(name='Алгебра')
    students_in_algebra = await Student.filter(
        enrollments__course=algebra_course
    ).distinct()
    print(f"Студентов на курсе Алгебра: {await students_in_algebra.count()}")

    # Получить расписание для группы "Группа А" на понедельник
    group_a = await Group.get(name='Группа А')
    monday_schedule = await Schedule.filter(
        group=group_a,
        day_of_week='Monday'
    )
    print(f"Занятий у Группы А в понедельник: {len(monday_schedule)}")

    # Получить задания, срок сдачи которых истекает в ближайшую неделю
    upcoming_assignments = await Assignment.filter(
        due_date__lte=date.today() + timedelta(days=7)
    )
    print(f"Заданий с ближайшим сроком сдачи: {len(upcoming_assignments)}")

    # Получить средний балл студентов по курсу "Алгебра"
    average_grade = await Enrollment.filter(
        course=algebra_course
    ).aggregate(average_grade='AVG(grade)')
    print(f"Средний балл по Алгебре: {average_grade['average_grade']}")

    # 2. Вставка данных

    async with transactions.in_transaction():
        new_students = []
        for i in range(100):
            user = await User.create(
                username=f'student_new_{i}',
                password='password123',
                email=f'student_new_{i}@example.com',
                first_name='Новый',
                last_name=f'Студент_{i}',
                role='student'
            )
            student = await Student.create(
                user=user,
                student_number=f'SN_{i}',
                enrollment_date=date.today()
            )
            new_students.append(student)

        # Записать новых студентов на курс "Алгебра"
        enrollments = [
            Enrollment(
                student=student,
                course=algebra_course,
                enrollment_date=date.today()
            )
            for student in new_students
        ]
        await Enrollment.bulk_create(enrollments)
    print("Добавлено 100 новых студентов и записано на курс 'Алгебра'.")

    # 3. Обновление данных

    await Enrollment.filter(
        course=algebra_course
    ).update(
        grade=F('grade') * 1.05
    )
    print("Оценки студентов по 'Алгебре' повышены на 5%.")

    # 4. Удаление данных

    one_year_ago = date.today() - timedelta(days=365)
    old_submissions = await Submission.filter(
        submission_date__lte=one_year_ago
    )
    deleted_count = await old_submissions.count()
    await old_submissions.delete()
    print(f"Удалено {deleted_count} старых ответов на задания.")

    end_time = time.time()
    print(f"Время выполнения запросов Tortoise ORM: {end_time - start_time} секунд.")

    await Tortoise.close_connections()

if __name__ == '__main__':
    run_async(run_queries())
