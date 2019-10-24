from django.contrib import admin
from django.db import models
from django.urls import path
from django.contrib import messages
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from adminlteui.widgets import AdminlteSelectMultiple
from .models import AnsibleTask, AnsibleTaskRecord, AnsibleTaskResponse
from .tasks import execute_ansible

# Register your models here.


class AnsibleTaskResponseTabularInline(admin.TabularInline):
    model = AnsibleTaskResponse
    readonly_fields = ('host', 'status', 'response', 'create_time')
    can_delete = False
    extra = 0
    ordering = ('-create_time',)


def execute_ansible_action(modeladmin, request, queryset):
    for obj in queryset:
        if obj.valid is True:
            execute_ansible(obj.id)
    messages.add_message(request, messages.SUCCESS,
                         _('{} Task processing.'.format(len(queryset))))


execute_ansible_action.short_description = _('Execute Selected Ansible Task')


@admin.register(AnsibleTask)
class AnsibleAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'args', 'valid',
                    'update_time', 'create_time')
    list_filter = ('valid', 'module')
    search_fields = ('name', 'description', 'args')
    list_editable = ('valid',)
    formfield_overrides = {
        models.ManyToManyField: {'widget': AdminlteSelectMultiple(attrs={
            'style': 'width: 100%;'
        })}
    }
    ordering = ('-create_time',)
    actions = [execute_ansible_action]


@admin.register(AnsibleTaskRecord)
class AnsibleTaskRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'ansible_task', 'display_hosts_number',
                    'display_response_number', 'update_time', 'create_time')
    list_filter = ('ansible_task__name',)
    search_fields = ('ansible_task__name', 'id')
    readonly_fields = ('id', 'ansible_task', 'create_time')
    inlines = [
        AnsibleTaskResponseTabularInline
    ]
    ordering = ('-create_time',)

    def display_hosts_number(self, obj):
        return obj.ansible_task.hosts.count()
    display_hosts_number.short_description = _('Hosts Number')

    def display_response_number(self, obj):
        return obj.ansibletaskresponse_set.count()
    display_response_number.short_description = _('Response Number')
