# utils/timing.py

import time

class TimeStamp:
    """
    Provides real-time and simulation-time timestamps.
    """

    @staticmethod
    def real_time():
        return time.time()

    @staticmethod
    def format_real(ts):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
