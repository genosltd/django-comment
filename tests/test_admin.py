from django.test import TestCase, RequestFactory
from django.urls import reverse

from django.contrib.auth.models import User, Permission
from django.contrib import admin

from django_comment import models
from .test_app.models import TestModel

from django_comment.admin import CommentedItemAdmin, CommentedItemInline


class CommentedItemAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.a_model = TestModel.objects.create()
        cls.author = User.objects.create(username='author')
        cls.superuser = User.objects.create(username='superuser',
                                            is_superuser=True)
        cls.request_factory = RequestFactory()
        url = reverse('admin:django_comment_commenteditem_add')
        cls.add_request = cls.request_factory.get(url)
        cls.commented_item_admin = CommentedItemAdmin(
            models.CommentedItem,
            admin.site
        )

    def test_item(self):
        comment = self.a_model.comments.create(comment='test comment',
                                               author=self.author)
        self.assertEqual(self.commented_item_admin.item(comment), self.a_model)

    def test_has_add_permission(self):
        self.assertFalse(self.commented_item_admin.has_add_permission(
            self.add_request
        ))

    def test_has_delete_permission_with_author(self):
        comment = self.a_model.comments.create(comment='test comment',
                                               author=self.author)
        url = reverse('admin:django_comment_commenteditem_delete',
                      args=(comment.id,))
        request = self.request_factory.get(url)
        request.user = self.author

        self.assertFalse(self.commented_item_admin.has_delete_permission(
            request, obj=comment
        ))

    def test_has_delete_permission_with_superuser(self):
        comment = self.a_model.comments.create(comment='test comment',
                                               author=self.author)
        url = reverse('admin:django_comment_commenteditem_delete',
                      args=(comment.id,))
        request = self.request_factory.get(url)
        request.user = self.superuser

        self.assertTrue(self.commented_item_admin.has_delete_permission(
            request, obj=comment
        ))


class CommentedItemInlineTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.a_model = TestModel.objects.create()
        cls.author = User.objects.create(username='author')
        cls.request_factory = RequestFactory()
        cls.commented_item_inline = CommentedItemInline(
            TestModel,
            admin.site
        )

    def test_has_change_permission(self):
        comment = self.a_model.comments.create(comment='test comment',
                                               author=self.author)
        url = reverse('admin:test_app_testmodel_change',
                      args=(self.a_model.id,))
        request = self.request_factory.get(url)
        request.user = self.author

        self.assertFalse(self.commented_item_inline.has_change_permission(
            request, obj=self.a_model
        ))


class HasCommentsAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.a_model = TestModel.objects.create()
        cls.author = User.objects.create(username='author', is_staff=True)
        permissions = set(Permission.objects.filter(
            codename__contains='testmodel'
        )) | set(Permission.objects.filter(
            codename__contains='commenteditem'
        ))
        cls.author.user_permissions.add(*permissions)

    def test_save_formset(self):
        url = reverse('admin:test_app_testmodel_change',
                      args=(self.a_model.id,))
        self.client.force_login(user=self.author)
        prefix = 'django_comment-commenteditem-content_type-object_id-'
        response = self.client.post(url, follow=True, data={
            prefix + 'TOTAL_FORMS': 1,
            prefix + 'INITIAL_FORMS': 0,
            prefix + '0-comment': 'test comment',
            '_continue': 'Save+and+continue+editing',
        })
        self.assertEqual(response.status_code, 200)
        comment = self.a_model.comments.first()

        self.assertEqual(comment.author, self.author)
