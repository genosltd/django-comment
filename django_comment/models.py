from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings


class CommentedItem(models.Model):
    class Meta:
        verbose_name = 'comment'

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, editable=False)
    posted_on = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.content_object} commented by {self.author} on " \
                    f"{self.posted_on}"


class HasComments(models.Model):
    comments = GenericRelation(CommentedItem)
