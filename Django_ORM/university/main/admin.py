from django.contrib import admin
from .models import User, Student, Teacher, Course, Group, Enrollment, Assignment, Submission, CourseMaterial, Schedule

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Group)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(CourseMaterial)
admin.site.register(Schedule)

