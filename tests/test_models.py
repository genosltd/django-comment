from django.test import TestCase

from django.contrib.auth.models import User

from django_comment import models
from .test_app.models import TestModel


class CommentedItemTestCase(TestCase):
    def test__str__(self):
        author = User.objects.create(username='author')
        a_model = TestModel.objects.create()
        comment = a_model.comments.create(comment='test comment', author=author)

        self.assertEqual(str(comment), 'test comment')
