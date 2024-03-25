from django.contrib import admin
from .models import Faculty, Class, TimeSlot, Day, Schedule

admin.site.register(Faculty)
admin.site.register(Class)
admin.site.register(TimeSlot)
admin.site.register(Day)
admin.site.register(Schedule)
