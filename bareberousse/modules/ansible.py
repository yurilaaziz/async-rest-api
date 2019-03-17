import os
import shutil
from collections import namedtuple

import git
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.utils.display import Display as DisplayBase
from ansible.vars.manager import VariableManager

from .base import BaseModule


def copy_project(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        raise Exception('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        raise Exception('Directory not copied. Error: %s' % e)


class Module(BaseModule):
    schema = {
        "playbook": {'type': 'string', 'required': True},
        "src": {'type': 'string', 'required': True},
        "extra_vars": {'type': 'dict', 'required': False},
        "inventory": {'type': 'string', 'required': False},
        "options": {'type': 'dict', 'required': False},
    }

    def main(self):
        playbook = self.args.get("playbook")
        src = self.args.get("src")
        project_src = os.path.join(self.temp_dir, "src")
        extra_vars = self.args.get("extra_vars", {})
        inventory = self.args.get("inventory", "inventory")
        options = self.args.get("options", {})

        Options = namedtuple('Options',
                             ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                              'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                              'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user',
                              'verbosity', 'check', 'diff'])

        playbook_options = Options(listtags=False,
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

        for key, value in options.items():
            setattr(playbook_options, key, value)

        def display(cls, msg, **kwargs):
            """ Forward output to module notification handler"""
            return self.notify(msg)

        DisplayBase.display = display
        DisplayBase.display = display

        if src.startswith("git+"):
            project_git_url = src[4:]
            git.Repo.clone_from(project_git_url, project_src)
        else:
            copy_project(src, project_src)

        inventory_file = project_src + "/" + inventory
        playbook_path = project_src + "/" + playbook

        loader = DataLoader()

        inventory_manager = InventoryManager(loader=loader, sources=inventory_file)
        variable_manager = VariableManager(loader=loader, inventory=inventory_manager)

        if not os.path.exists(playbook_path):
            self.notify("[INFO] The playbook does not exist")
            self.state.failed()
            return

        variable_manager.extra_vars = extra_vars

        passwords = {}

        pbex = PlaybookExecutor(playbooks=[playbook_path],
                                inventory=inventory_manager,
                                variable_manager=variable_manager,
                                loader=loader,
                                options=playbook_options,
                                passwords=passwords)
        # global display

        result = pbex.run()

        if result == 0:
            self.state.success()
        else:
            self.state.failed()
