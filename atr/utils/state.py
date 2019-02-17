class State:
    def __init__(self):
        self.state = Pending

    def switch(self, new_state):
        if not issubclass(new_state, BaseState):
            raise TypeError("New State '{}' is not a subclass of '{}'".format(new_state, BaseState))
        if new_state == self.state:
            pass
        elif new_state in self.state.allowed:
            self.state = new_state
        else:
            raise TypeError(
                "Current state could not be switched from {} to  {}".format(self.state.__name__, new_state.__name__))

    def success(self):
        self.switch(Success)

    def failed(self):
        self.switch(Failed)

    def error(self):
        self.switch(Error)

    def running(self):
        self.switch(Running)

    def pending(self):
        self.switch(Pending)

    def initializing(self):
        self.switch(Initializing)

    def __str__(self):
        return self.state.__name__

    def __dict__(self):
        return self.__str__()


class BaseState:
    allowed = []


class Success(BaseState):
    allowed = []


class Failed(BaseState):
    allowed = []


class Error(BaseState):
    allowed = []


class Running(BaseState):
    allowed = [Success, Failed, Error]


class Initializing(BaseState):
    allowed = [Running, Error]


class Pending(BaseState):
    allowed = [Initializing, Error]
