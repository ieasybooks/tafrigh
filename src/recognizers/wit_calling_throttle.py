import time

from multiprocessing.managers import BaseManager
from threading import Lock


class WitCallingThrottle:
    def __init__(self, wit_client_access_tokens_count: int, call_times_limit: int = 1, expired_time: int = 1):
        self.wit_client_access_tokens_count = wit_client_access_tokens_count
        self.call_times_limit = call_times_limit
        self.expired_time = expired_time
        self.call_timestamps = [[] for _ in range(self.wit_client_access_tokens_count)]
        self.locks = [Lock() for _ in range(self.wit_client_access_tokens_count)]

    def throttle(self, wit_client_access_token_index: int) -> None:
        with self.locks[wit_client_access_token_index]:
            while len(self.call_timestamps[wit_client_access_token_index]) == self.call_times_limit:
                now = time.time()

                self.call_timestamps[wit_client_access_token_index] = list(
                    filter(
                        lambda call_timestamp, now=now: now - call_timestamp < self.expired_time,
                        self.call_timestamps[wit_client_access_token_index],
                    )
                )

                if len(self.call_timestamps[wit_client_access_token_index]) == self.call_times_limit:
                    time_to_sleep = self.call_timestamps[wit_client_access_token_index][0] + self.expired_time - now
                    time.sleep(time_to_sleep)

            self.call_timestamps[wit_client_access_token_index].append(time.time())


class WitCallingThrottleManager(BaseManager):
    pass


WitCallingThrottleManager.register('WitCallingThrottle', WitCallingThrottle)
