#!env python

import time
# note:
# from 2020/09/10,
# The Pacer method is no longer recommended to consume pcm data.
# It is recommended to use AudioConsumer to consume pcm data(or push generated pcm data to rtc)
import asyncio
import logging
logger = logging.getLogger(__name__)


class Pacer:
    def __init__(self, interval):
        self.last_call_time = time.time()
        self.interval = interval

    def pace(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time
        if elapsed_time < self.interval:
            time.sleep(self.interval - elapsed_time)
            # print("sleep time:", (self.interval - elapsed_time)*1000)
        self.last_call_time = time.time()

    def pace_interval(self, time_interval_s):
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time
        if elapsed_time < time_interval_s:
            time.sleep(time_interval_s - elapsed_time)
            # print("sleep time(ms):", (time_interval_s - elapsed_time)*1000)
        self.last_call_time = time.time()

    async def apace_interval(self, time_interval_s):
        current_time = time.time()
        elapsed_time = current_time - self.last_call_time
        # logger.info(f"elapsed_time:{elapsed_time}, time_interval_s:{time_interval_s}")
        if elapsed_time < time_interval_s:
            await asyncio.sleep(time_interval_s - elapsed_time)
        self.last_call_time = time.time()
