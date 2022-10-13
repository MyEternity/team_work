from django.contrib import admin
from .models import User, UserProfile
from django_summernote.admin import SummernoteModelAdmin


class InfoAdmin(SummernoteModelAdmin):
    summernote_fields = ('about',)


# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile, InfoAdmin)
