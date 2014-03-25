from __future__ import absolute_import, division, print_function, unicode_literals

class Channel(object):

    def __init__(self, name, bounds=(float('-inf'), float('+inf'))):
        self.name = name
        self.bounds = bounds

