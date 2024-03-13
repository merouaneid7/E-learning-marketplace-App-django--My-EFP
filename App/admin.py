from django.contrib import admin
from .models import *
# Register your models here.

class objectif_TabularInlaine(admin.TabularInline):
    model = objectif

class Video_TabularInlaine(admin.TabularInline):
    model = Video

class course_admin(admin.ModelAdmin):
    inlines = (objectif_TabularInlaine,Video_TabularInlaine)





admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,course_admin)
admin.site.register(Level)
admin.site.register(objectif)
admin.site.register(lesson)
admin.site.register(Video)
admin.site.register(Language)
admin.site.register(UserCourse)


