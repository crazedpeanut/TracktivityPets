from django.contrib import admin

from .models import UserFitbit

class UserFitbitAdmin(admin.ModelAdmin):
    fields=('user',)

admin.site.register(UserFitbit, UserFitbitAdmin)

