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



class Module(BaseModule):
    schema = {
        "state": {'type': 'string', 'required': False},
        "message": {'type': 'string', 'required': True},
    }

    def main(self):
        self.notify(self.args.get("message"))

        if self.args.get("state", "").lower() == "success":
            self.state.success()
        elif self.args.get("state", "").lower() == "failed":
            self.state.failed()
