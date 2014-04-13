from __future__ import absolute_import, division, print_function

class UnidirectionalHub(object):
    """A class for distributing data unidirectionally"""

    def __init__(self, receivers=()):
        self.receivers = list(receivers)

    def register(self, receiver):
        self.receivers.append(receiver)

    def receive(self, data):
        for receiver in self.receivers:
            receiver(data)

class BidirectionalHub(object):
    """A class for polling other object with a request"""

    def __init__(self, receivers=()):
        self.receivers = list(receivers)

    def register(self, receiver):
        self.receivers.append(receiver)

    def poll(self, data):
        answers = []
        for receiver in self.receivers:
            answers.append(receiver(data))
        return answers
