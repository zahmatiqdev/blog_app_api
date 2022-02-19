from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User, Post, Tag


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = [
        "id",
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    ]
    list_filter = [
        "published",
        "publish_date",
    ]
    list_editable = [
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    ]
    search_fields = [
        "title",
        "subtitle",
        "slug",
        "body",
    ]
    prepopulated_fields = {
        "slug": [
            "title",
            "subtitle",
        ]
    }
    date_hierarchy = "publish_date"
    save_on_top = True


admin.site.register(User, UserAdmin)
