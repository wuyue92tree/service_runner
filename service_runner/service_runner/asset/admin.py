from django.contrib import admin
from django import forms
from django.db import models
from .models import Host, HostGroup
# Register your models here.


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    pass


@admin.register(HostGroup)
class HostGroupAdmin(admin.ModelAdmin):
    pass
