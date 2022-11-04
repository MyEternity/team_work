from django.contrib import admin
from django_summernote.admin import SummernoteInlineModelAdmin

from .models import User, UserProfile


class UserProfileInline(SummernoteInlineModelAdmin, admin.StackedInline):
    model = UserProfile
    summernote_fields = ('about',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)
    filter_horizontal = ['groups', 'user_permissions', ]
