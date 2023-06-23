class BaseState(object):
    def __init__(self, state):
        self.state = state

    def current(self):
        return self.state

    def next_step(self):
        raise NotImplementedError
