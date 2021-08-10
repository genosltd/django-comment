from django.contrib import admin
from django_comment.admin import HasCommentsAdmin

from . import models


@admin.register(models.ExampleModel)
class ExampleModelAdmin(HasCommentsAdmin):
    pass
