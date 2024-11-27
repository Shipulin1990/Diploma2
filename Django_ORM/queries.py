# django_orm/queries.py

import os
import django
import time
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university.settings')
django.setup()

from main.models import (
    Student, Course, Enrollment, Assignment, Submission,
    Schedule, Group, User
)
from django.db.models import Avg, F
from datetime import timedelta
from django.db import transaction

def run_queries():
    start_time = time.time()

    # 1. Выборка данных

    # Получить всех студентов, записанных на курс "Алгебра"
    algebra_course = Course.objects.get(name='Алгебра')
    students_in_algebra = Student.objects.filter(enrollment__course=algebra_course)
    print(f"Студентов на курсе Алгебра: {students_in_algebra.count()}")

    # Получить расписание для группы "Группа А" на понедельник
    group_a = Group.objects.get(name='Группа А')
    monday_schedule = Schedule.objects.filter(group=group_a, day_of_week='Monday')
    print(f"Занятий у Группы А в понедельник: {monday_schedule.count()}")

    # Получить задания, срок сдачи которых истекает в ближайшую неделю
    upcoming_assignments = Assignment.objects.filter(
        due_date__lte=timezone.now() + timedelta(days=7)
    )
    print(f"Заданий с ближайшим сроком сдачи: {upcoming_assignments.count()}")

    # Получить средний балл студентов по курсу "Алгебра"
    average_grade = Enrollment.objects.filter(course=algebra_course).aggregate(Avg('grade'))
    print(f"Средний балл по Алгебре: {average_grade['grade__avg']}")

    # 2. Вставка данных

    with transaction.atomic():
        new_students = []
        for i in range(100):
            user = User.objects.create_user(
                username=f'student_new_{i}',
                password='password123',
                email=f'student_new_{i}@example.com',
                first_name='Новый',
                last_name=f'Студент_{i}',
                role='student'
            )
            student = Student.objects.create(
                user=user,
                student_number=f'SN_{i}',
                enrollment_date=timezone.now()
            )
            new_students.append(student)

        # Записать новых студентов на курс "Алгебра"
        enrollments = [
            Enrollment(student=student, course=algebra_course, enrollment_date=timezone.now())
            for student in new_students
        ]
        Enrollment.objects.bulk_create(enrollments)
    print("Добавлено 100 новых студентов и записано на курс 'Алгебра'.")

    # 3. Обновление данных

    # Повысить оценки на 5%
    Enrollment.objects.filter(course=algebra_course).update(
        grade=F('grade') * 1.05
    )
    print("Оценки студентов по 'Алгебре' повышены на 5%.")

    # 4. Удаление данных

    one_year_ago = timezone.now() - timedelta(days=365)
    old_submissions = Submission.objects.filter(submission_date__lte=one_year_ago)
    deleted_count = old_submissions.count()
    old_submissions.delete()
    print(f"Удалено {deleted_count} старых ответов на задания.")

    end_time = time.time()
    print(f"Время выполнения запросов Django ORM: {end_time - start_time} секунд.")

if __name__ == '__main__':
    run_queries()
