from django.contrib import admin

from django.contrib import admin

from .models import Question, Choice

admin.site.register(Question)  # Add the Question model to the admin for easier access.

admin.site.register(Choice)  # Add the Choice model to the admin for easier access. This is not included in Django tutorial.
