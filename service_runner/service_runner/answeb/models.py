from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from service_runner.service_runner.asset.models import Host


# Create your models here.


class AnsibleTask(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(
        blank=True, null=True, verbose_name=_('Description'))
    hosts = models.ManyToManyField(Host, verbose_name=_('Hosts'))
    module = models.CharField(
        default='shell', max_length=255, verbose_name=_('Module'))
    args = models.TextField(verbose_name=_('Args'))
    valid = models.BooleanField(default=True, verbose_name=_('Valid'))
    create_time = models.DateTimeField(
        default=timezone.now, verbose_name=_('createTime'))
    update_time = models.DateTimeField(
        auto_now=True, verbose_name=_('updateTime')
    )

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Ansible Task')
        verbose_name_plural = _('Ansible Tasks')


class AnsibleTaskRecord(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, auto_created=True,
                          verbose_name=_('Id'))
    ansible_task = models.ForeignKey(
        AnsibleTask, on_delete=models.CASCADE, verbose_name=_('ansibleTask'))
    create_time = models.DateTimeField(
        default=timezone.now, verbose_name=_('createTime'))
    update_time = models.DateTimeField(
        auto_now=True, verbose_name=_('updateTime')
    )

    def __str__(self):
        return '{}_{}'.format(self.id, self.ansible_task)

    class Meta:
        verbose_name = _('Ansible Task Record')
        verbose_name_plural = _('Ansible Task Records')


class AnsibleTaskResponse(models.Model):
    STATUS_CHOICE = (
        ('success', _('SUCCESS')),
        ('failed', _('FAILED')),
        ('unreachable', _('UNREACHABLE')),
    )
    ansible_task_record = models.ForeignKey(
        AnsibleTaskRecord, on_delete=models.CASCADE, verbose_name=_('ansibleTaskRecord'))
    host = models.ForeignKey(
        Host, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Host')
    )
    status = models.CharField(
        default='success', choices=STATUS_CHOICE, max_length=255, verbose_name=_('Status'))
    response = models.TextField(
        blank=True, null=True, verbose_name=_('Response'))
    create_time = models.DateTimeField(
        default=timezone.now, verbose_name=_('createTime'))
    update_time = models.DateTimeField(
        auto_now=True, verbose_name=_('updateTime')
    )

    def __str__(self):
        return '{}'.format(self.ansible_task_record)

    class Meta:
        verbose_name = _('Ansible Task Response')
        verbose_name_plural = _('Ansible Task Responses')
