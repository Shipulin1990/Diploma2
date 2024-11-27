from tortoise import fields, models
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
class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)
    email = fields.CharField(max_length=100, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    role = fields.CharEnumField(UserRole)

    # Отношения
    student: fields.ReverseRelation["Student"]
    teacher: fields.ReverseRelation["Teacher"]

# 2. Студенты
class Student(models.Model):
    user = fields.OneToOneField('models.User', on_delete=fields.CASCADE, related_name='student', pk=True)
    student_number = fields.CharField(max_length=20, unique=True)
    enrollment_date = fields.DateField()

    # Отношения
    enrollments: fields.ReverseRelation["Enrollment"]
    submissions: fields.ReverseRelation["Submission"]
    groups: fields.ManyToManyRelation["Group"]

# 3. Преподаватели
class Teacher(models.Model):
    user = fields.OneToOneField('models.User', on_delete=fields.CASCADE, related_name='teacher', pk=True)
    employee_number = fields.CharField(max_length=20, unique=True)
    hire_date = fields.DateField()
    department = fields.CharField(max_length=100)

    # Отношения
    courses: fields.ReverseRelation["TeacherCourse"]
    schedules: fields.ReverseRelation["Schedule"]

# 4. Курсы
class Course(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField()
    credits = fields.IntField()

    # Отношения
    assignments: fields.ReverseRelation["Assignment"]
    materials: fields.ReverseRelation["CourseMaterial"]
    enrollments: fields.ReverseRelation["Enrollment"]
    teachers: fields.ReverseRelation["TeacherCourse"]
    schedules: fields.ReverseRelation["Schedule"]

# 5. Группы
class Group(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    year = fields.IntField()

    # Отношения
    students: fields.ManyToManyRelation["Student"] = fields.ManyToManyField(
        'models.Student', related_name='groups', through='student_groups'
    )
    schedules: fields.ReverseRelation["Schedule"]

# 6. Записи студентов в группы (многие-ко-многим) — через связную таблицу 'student_groups', которая создается автоматически.

# 7. Преподаватели и Курсы (многие-ко-многим)
class TeacherCourse(models.Model):
    id = fields.IntField(pk=True)
    teacher = fields.ForeignKeyField('models.Teacher', on_delete=fields.CASCADE, related_name='courses')
    course = fields.ForeignKeyField('models.Course', on_delete=fields.CASCADE, related_name='teachers')

    class Meta:
        unique_together = ('teacher', 'course')

# 8. Записи студентов на курсы
class Enrollment(models.Model):
    id = fields.IntField(pk=True)
    student = fields.ForeignKeyField('models.Student', on_delete=fields.CASCADE, related_name='enrollments')
    course = fields.ForeignKeyField('models.Course', on_delete=fields.CASCADE, related_name='enrollments')
    enrollment_date = fields.DateField()
    grade = fields.FloatField(null=True)

    class Meta:
        unique_together = ('student', 'course')

# 9. Задания
class Assignment(models.Model):
    id = fields.IntField(pk=True)
    course = fields.ForeignKeyField('models.Course', on_delete=fields.CASCADE, related_name='assignments')
    title = fields.CharField(max_length=200)
    description = fields.TextField()
    due_date = fields.DateField()

    # Отношения
    submissions: fields.ReverseRelation["Submission"]

# 10. Ответы на задания
class Submission(models.Model):
    id = fields.IntField(pk=True)
    assignment = fields.ForeignKeyField('models.Assignment', on_delete=fields.CASCADE, related_name='submissions')
    student = fields.ForeignKeyField('models.Student', on_delete=fields.CASCADE, related_name='submissions')
    submission_date = fields.DateField()
    file_path = fields.CharField(max_length=255)
    grade = fields.FloatField(null=True)

    class Meta:
        unique_together = ('assignment', 'student')

# 11. Материалы курса
class CourseMaterial(models.Model):
    id = fields.IntField(pk=True)
    course = fields.ForeignKeyField('models.Course', on_delete=fields.CASCADE, related_name='materials')
    title = fields.CharField(max_length=200)
    material_type = fields.CharEnumField(MaterialType)
    file_path = fields.CharField(max_length=255)

# 12. Расписание
class Schedule(models.Model):
    id = fields.IntField(pk=True)
    course = fields.ForeignKeyField('models.Course', on_delete=fields.CASCADE, related_name='schedules')
    group = fields.ForeignKeyField('models.Group', on_delete=fields.CASCADE, related_name='schedules')
    teacher = fields.ForeignKeyField('models.Teacher', on_delete=fields.CASCADE, related_name='schedules')
    classroom = fields.CharField(max_length=50)
    start_time = fields.TimeField()
    end_time = fields.TimeField()
    day_of_week = fields.CharEnumField(DayOfWeek)

    class Meta:
        unique_together = ('course', 'group', 'teacher', 'day_of_week', 'start_time')

