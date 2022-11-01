from django.contrib import admin
from .models import User, UserProfile
from django_summernote.admin import SummernoteInlineModelAdmin


class UserProfileInline(SummernoteInlineModelAdmin, admin.StackedInline):
    model = UserProfile
    summernote_fields = ('about',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline, )
    filter_horizontal = ['groups', 'user_permissions', ]
