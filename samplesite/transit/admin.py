from django.contrib import admin

from .models import Request


class UserAdmin(admin.ModelAdmin):
    list_display = ('user',)


class RequestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'direction', 'type', 'time', 'weight', 'measure_name', 'author')
    list_display_links = ('pk', 'name', 'direction', 'type', 'time', 'weight', 'measure_name', 'author')


admin.site.register(Request, RequestAdmin,)
