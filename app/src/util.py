import time as tm


class Stopwarch(object):

    def __init__(self, unit='ms', multiplier=1000):
        self.start_time = tm.time()
        self.multiplier = multiplier
        self.unit = unit

    def time_with_unit(self):
        duration = (tm.time() - self.start_time) * self.multiplier
        self.duration = duration
        return duration, self.unit

    def time(self):
        return self.time_with_unit()[0]

    def and_end(self):
        self.time()
        return self

    def and_start(self):
        self.start_time = tm.time()
        return self

    def start(self):
        self.start_time = tm.time()
