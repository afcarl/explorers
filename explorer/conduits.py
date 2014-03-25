from __future__ import absolute_import, division, print_function, unicode_literals

class Hub(object):
    """A class for distributing data"""

    def __init__(self, receivers=()):
        self.receivers = list(receivers)

    def register(self, receiver):
        self.receivers.append(receiver)

    def receive(self, data):
        for receiver in self.receivers:
            receiver(data)