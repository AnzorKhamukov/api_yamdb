from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'role')
    search_fields = ('username',)
    empty_value_display = '-пусто-'
    list_filter = ('username',)


admin.site.register(User)
