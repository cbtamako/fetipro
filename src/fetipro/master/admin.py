# encoding=utf-8

from django.contrib import admin
from fetipro.master.models import Feti


class FetiAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "parent")

admin.site.register(Feti, FetiAdmin)


