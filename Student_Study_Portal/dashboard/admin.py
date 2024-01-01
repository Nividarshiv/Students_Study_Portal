from django.contrib import admin
from dashboard.models import Note,Homework,Todo

# Register your models here.
admin.site.register(Note)
admin.site.register(Homework)
admin.site.register(Todo)
