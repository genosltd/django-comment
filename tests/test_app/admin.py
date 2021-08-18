from django.contrib import admin
from django_comment import admin as django_comment_admin

from . import models


@admin.register(models.TestModel)
class TestModelAdmin(django_comment_admin.HasCommentsAdmin):
    pass
