class BaseState:
    allowed = []

    def __str__(self):
        return self.__name__

    def __dict__(self):
        return self.__str__()


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


class State:
    Pending = Pending
    Initializing = Initializing
    Running = Running
    Error = Error
    Failed = Failed
    Success = Success

    def __init__(self, state):
        self.state = None
        if not state:
            self.state = Pending
        elif isinstance(state, str):
            self.from_string(state)
        elif issubclass(state, BaseState):
            self.state = state
        else:
            raise TypeError("New State '{}' is not a subclass of '{}'".format(state, BaseState))

    def from_string(self, status):
        state_cls = getattr(self, status, None)
        if state_cls:
            if self.state:
                self.switch(state_cls)
            else:
                self.state = state_cls
        else:
            raise TypeError("State '{}' is not defined".format(status))

    def is_final(self):
        return len(self.state.allowed) == 0

    def is_equal(self, state):
        return self.state == state

    def switch(self, new_state):
        if not issubclass(new_state, BaseState):
            raise TypeError("New State '{}' is not a subclass of '{}'".format(new_state, BaseState))
        if new_state == self.state:
            pass
        elif new_state in self.state.allowed:
            self.state = new_state
        else:
            raise TypeError(
                "Current state could not be switched from {} to  {}"
                "".format(self.state.__name__, new_state.__name__))

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
