from __future__ import absolute_import, division, print_function, unicode_literals

class Channel(object):

    def __init__(self, name, bounds=(float('-inf'), float('+inf'))):
        self.name = name
        self.bounds = bounds

    def __repr__(self):
        return 'Channel({}, {})'.format(self.name, self.bounds)

    def __eq__(self, channel):
        return self.name == channel.name and self.bounds == channel.bounds
