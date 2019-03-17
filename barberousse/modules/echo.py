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
