import os
import json
import sys
import logging
import traceback

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
# from ansible.utils.sentinel import Sentinel

# logger = logging.basicConfig()


class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


# class MyInventory(object):
#     """
#     this is my ansible inventory object.
#     """

#     def __init__(self, resource, loader, variable_manager):
#         """
#         resource的数据格式是一个列表字典，比如
#             {
#                 "group1": {
#                     "hosts": [{"hostname": "10.0.0.0", "port": "22",
#                     "username": "test", "password": "pass"}, ...],
#                     "vars": {"var1": value1, "var2": value2, ...}
#                 }
#             }
#         如果你只传入1个列表，这默认该列表内的所有主机属于my_group组,比如
#             [{"hostname": "10.0.0.0", "port": "22", "username": "test",
#              "password": "pass"}, ...]
#         """
#         self.resource = resource
#         self.inventory = Inventory(loader=loader,
#                                    variable_manager=variable_manager,
#                                    host_list=[])
#         self.gen_inventory()

#     def my_add_group(self, hosts, groupname, groupvars=None):
#         """
#         add hosts to a group
#         """
#         my_group = Group(name=groupname)

#         # if group variables exists, add them to group
#         if groupvars:
#             for key, value in groupvars.iteritems():
#                 my_group.set_variable(key, value)

#                 # add hosts to group
#         for host in hosts:
#             # set connection variables
#             hostname = host.get("hostname")
#             hostip = host.get('ip', hostname)
#             hostport = host.get("port")
#             username = host.get("username")
#             password = host.get("password")
#             ssh_key = host.get("ssh_key")
#             my_host = Host(name=hostname, port=hostport)
#             my_host.set_variable('ansible_ssh_host', hostip)
#             my_host.set_variable('ansible_ssh_port', hostport)
#             my_host.set_variable('ansible_ssh_user', username)
#             my_host.set_variable('ansible_ssh_pass', password)
#             my_host.set_variable('ansible_ssh_private_key_file', ssh_key)

#             # set other variables
#             for key, value in host.iteritems():
#                 if key not in ["hostname", "port", "username", "password"]:
#                     my_host.set_variable(key, value)
#                     # add to group
#             my_group.add_host(my_host)

#         self.inventory.add_group(my_group)

#     def gen_inventory(self):
#         """
#         add hosts to inventory.
#         """
#         if isinstance(self.resource, list):
#             self.my_add_group(self.resource, 'default_group')
#         elif isinstance(self.resource, dict):
#             for groupname, hosts_and_vars in self.resource.iteritems():
#                 self.my_add_group(hosts_and_vars.get("hosts"), groupname,
#                                   hosts_and_vars.get("vars"))


class AnsibleApi(object):
    """
    This is a General object for parallel execute modules.
    """

    def __init__(self, resource, *args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.results_raw = {}

    def create_options(self, connection='smart',
                       module_path=None, forks=100,
                       timeout=10,
                       remote_user='root',
                       ask_pass=False,
                       private_key_file=None,
                       ssh_common_args='-o StrictHostKeyChecking=no',
                       ssh_extra_args=None,
                       sftp_extra_args=None, scp_extra_args=None,
                       become=None, become_method=None,
                       become_user='root', ask_value_pass=False,
                       verbosity=None, check=False, listhosts=False,
                       listtasks=False, listtags=False, syntax=False, diff=True):
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'timeout',
                              'remote_user',
                              'ask_pass', 'private_key_file',
                              'ssh_common_args', 'ssh_extra_args',
                              'sftp_extra_args',
                              'scp_extra_args', 'become', 'become_method',
                              'become_user', 'ask_value_pass',
                              'verbosity',
                              'check', 'listhosts', 'listtasks', 'listtags',
                              'syntax', 'diff'])

        return Options(connection=connection,
                       module_path=module_path, forks=forks,
                       timeout=timeout,
                       remote_user=remote_user,
                       ask_pass=ask_pass,
                       private_key_file=private_key_file,
                       ssh_common_args=ssh_common_args,
                       ssh_extra_args=ssh_extra_args,
                       sftp_extra_args=sftp_extra_args, scp_extra_args=scp_extra_args,
                       become=become, become_method=become_method,
                       become_user=become_user, ask_value_pass=ask_value_pass,
                       verbosity=verbosity, check=check, listhosts=listhosts,
                       listtasks=listtasks, listtags=listtags, syntax=syntax, diff=diff)

    def initializeData(self):
        """
        初始化ansible
        """
        # initialize needed objects
        self.loader = DataLoader()
        self.options = self.create_options() if not self.options else self.options
        self.passwords = dict(
            sshpass=None, becomepass=None) if not self.passwords else self.passwords
        self.inventory = InventoryManager(
            loader=self.loader, sources=self.resource)
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

    def run(self, host, module_name, module_args):
        """
        run module from ansible ad-hoc.
        module_name: ansible module_name
        module_args: ansible module args
        """
        # create play with tasks
        play_source = dict(
            name="Ansible Play",
            hosts=host,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager,
                           loader=self.loader)

        # actually run it
        tqm = None
        self.callback = ResultCallback()
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.callback
            )
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, host, playbooks, **extra_vars):
        """
        run ansible playbook
        """
        try:
            self.callback = ResultCallback()
            _extra_vars = {}
            _extra_vars['host'] = host
            for k, v in extra_vars:
                _extra_vars[k] = v
            self.variable_manager.extra_vars = _extra_vars
            print(self.variable_manager.extra_vars)
            executor = PlaybookExecutor(
                playbooks=playbooks,
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.callback
            executor.run()
        except Exception as e:
            traceback.print_exc()

    def get_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'][host] = result._result.get(
                'msg') or result._result

        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result['msg']

        return self.results_raw
