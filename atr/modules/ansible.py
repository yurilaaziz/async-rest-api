import os
from collections import namedtuple

import ansible
import git
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.utils.display import Display as DisplayBase
from ansible.vars.manager import VariableManager

from .base import BaseModule


class Display(DisplayBase):
    def display(self, msg, color=None, stderr=False, screen_only=False, log_only=False):
        """ Forward output to database"""
        # print(">> ({}) >> {}".format(len(msg),msg))
        pass


ansible.executor.playbook_executor.display = Display(verbosity=3)
ansible.parsing.vault.display = Display(verbosity=3)

import shutil
import tempfile


def copy_project(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


class Module(BaseModule):
    def main(self):
        playbook = "site.yml"
        src = "/Users/yuri/workspace/flask-cloudnative/examples/ansible"
        tmp_dir = tempfile.mkdtemp()
        project_src = os.path.join(tmp_dir, "src")
        extra_vars = {'user': 'mywebserver'}

        Options = namedtuple('Options',
                             ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                              'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                              'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user',
                              'verbosity', 'check', 'diff'])
        options = Options(listtags=False,
                          listtasks=False,
                          listhosts=False,
                          syntax=False,
                          connection='ssh',
                          module_path=None,
                          forks=100,
                          remote_user="barberousse",
                          private_key_file=None,
                          ssh_common_args=None,
                          ssh_extra_args=None,
                          sftp_extra_args=None,
                          scp_extra_args=None,
                          become=True,
                          become_method='sudo',
                          become_user='root',
                          verbosity=None,
                          check=False,
                          diff=False)
        for key, value in self.args.get("options", {}).items():
            setattr(options, key, value)

        def display(cls, msg, **kwargs):
            """ Forward output to module notification handler"""
            return self.notify(msg)

        DisplayBase.display = display

        if src.startswith("git+"):
            project_git_url = src[4:]
            git.Repo.clone_from(project_git_url, project_src)
        else:
            copy_project(src, project_src)

        inventory_file = project_src + "/inventory"
        playbook_path = project_src + "/" + playbook

        loader = DataLoader()

        inventory_manager = InventoryManager(loader=loader, sources=inventory_file)
        variable_manager = VariableManager(loader=loader, inventory=inventory_manager)

        if not os.path.exists(playbook_path):
            self.notify("[INFO] The playbook does not exist")
            self.state.failed()
            return

        variable_manager.extra_vars = extra_vars  # This can accomodate various other command line arguments.`

        passwords = {}

        pbex = PlaybookExecutor(playbooks=[playbook_path],
                                inventory=inventory_manager,
                                variable_manager=variable_manager,
                                loader=loader,
                                options=options,
                                passwords=passwords)
        # global display

        result = pbex.run()

        if result == 0:
            self.state.success()
        else:
            self.state.failed()
