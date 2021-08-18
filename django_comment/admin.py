from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from django.db.models.functions import Concat
from django.db.models import Value

from . import models


@admin.register(models.CommentedItem)
class CommentedItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'author', 'posted_on', 'comment')
    ordering = ('posted_on',)
    readonly_fields = ('content_object', 'author', 'posted_on')

    def item(self, obj):
        return obj.content_object

    item.admin_order_field = Concat('content_type', Value(' '), 'object_id')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    has_delete_permission = has_change_permission


class CommentedItemInline(GenericStackedInline):
    model = models.CommentedItem
    readonly_fields = ('author', 'posted_on')
    fields = ('author', 'posted_on', 'comment')
    extra = 1
    can_delete = False
    ordering = ('posted_on',)

    def has_change_permission(self, request, obj=None):
        return False


class HasCommentsAdmin(admin.ModelAdmin):
    inlines = (CommentedItemInline,)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.new_objects:
            obj.author = request.user
            obj.save()
        super().save_formset(request, form, formset, change)
