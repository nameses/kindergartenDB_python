from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.UserAdditionInfo)
admin.site.register(models.Kindergarten)
admin.site.register(models.KindergartenGroup)
admin.site.register(models.Child)
admin.site.register(models.Month)
admin.site.register(models.Attendance)
