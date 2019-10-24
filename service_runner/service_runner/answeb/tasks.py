import uuid
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from celery import shared_task
from service_runner.service_runner.answeb.ansible_api import AnsibleApi
from service_runner.service_runner.answeb.models import AnsibleTask, AnsibleTaskRecord, AnsibleTaskResponse


def format_result(host, result):
    callback = {}
    if result.get('success'):
        callback['message'] = 'success'
        callback['data'] = result.get('success').get(host.ip)
    elif result.get('failed'):
        callback['message'] = 'failed'
        callback['data'] = result.get('failed').get(host.ip)
    elif result.get('unreachable'):
        callback['message'] = 'unreachable'
        callback['data'] = result.get('unreachable').get(host.ip)
    return callback


def call_ansible_api(host, module, args):
    api = AnsibleApi(resource=host.ip + ',')
    if host.ssh_key:
        api.options = api.create_options(remote_user=host.ssh_user,
                                         private_key_file=host.ssh_key.ssh_key.path)
    else:
        api.options = api.create_options(remote_user=host.ssh_user)
        api.passwords = dict(sshpass=host.ssh_passwd)

    api.initializeData()
    api.run(host.ip, module, args)
    result = api.get_result()
    return format_result(host, result)


@shared_task
def execute_ansible(ansible_task_id):
    task = AnsibleTask.objects.get(id=ansible_task_id)
    _uuid = str(uuid.uuid4())
    task_record = AnsibleTaskRecord.objects.create(
        id=_uuid, ansible_task_id=task.id
    )
    host_list = task.hosts.all()

    for host in host_list:
        if host.valid is False:
            response = {
                'message': 'failed',
                'data': _('host valid is False. skip'),
            }

        else:
            response = call_ansible_api(host, task.module, task.args)

        AnsibleTaskResponse.objects.create(
            ansible_task_record=task_record, host=host, response=response.get(
                'data'),
            status=response.get('message')
        )
