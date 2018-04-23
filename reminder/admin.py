from django.contrib import admin

from .models import *


def refresh_content(modeladmin, request, queryset):
    for token in queryset:
        token.get_content()
        token.save()


refresh_content.short_description = '重新抓取 内容'


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['order', 'name', 'update_time']
    search_fields = ('order', 'name',)
    actions = [refresh_content]


admin.site.register(Chapter, ChapterAdmin)
