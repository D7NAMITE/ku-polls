from django.contrib import admin

from django.contrib import admin

from .models import Question, Choice

admin.site.register(Question)

admin.site.register(Choice)  # This is the 'Choice' registration for the admin.
