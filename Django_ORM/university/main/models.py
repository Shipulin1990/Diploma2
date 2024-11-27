from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Пользователи
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('administrator', 'Администратор'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

# 2. Студенты
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_number = models.CharField(max_length=20, unique=True)
    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()}"

# 3. Преподаватели
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_number = models.CharField(max_length=20, unique=True)
    hire_date = models.DateField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()}"

# 4. Курсы
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField()

    def __str__(self):
        return self.name

# 5. Группы
class Group(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.name

# 6. Записи студентов в группы (многие-ко-многим)
class StudentGroup(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'group')

# 7. Преподаватели и Курсы (многие-ко-многим)
class TeacherCourse(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'course')

# 8. Записи студентов на курсы
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

# 9. Задания
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.title

# 10. Ответы на задания
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submission_date = models.DateField()
    file = models.FileField(upload_to='submissions/')
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('assignment', 'student')

# 11. Материалы курса
class CourseMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('lecture', 'Лекция'),
        ('presentation', 'Презентация'),
        ('document', 'Документ'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES)
    file = models.FileField(upload_to='course_materials/')

    def __str__(self):
        return self.title

# 12. Расписание
class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
        ('Saturday', 'Суббота'),
        ('Sunday', 'Воскресенье'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f"{self.course.name} - {self.day_of_week}"


