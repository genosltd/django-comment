from django.db import models
from django_comment import models as django_comment_models


class TestModel(django_comment_models.HasComments):
    test_field = models.CharField(max_length=100, blank=True, null=True)
