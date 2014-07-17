import time
import urllib2
import uuid
import threading

import utils.logger as log


def wait_for_internet_connection():
    """Checks for internet connection every 20 seconds. Goes into infinite
    loop until connection is found.
    """
    while True:
        try:
            urllib2.urlopen('http://www.google.com', timeout=3)
            log.debug('Internet connection detected.')
            return

        except urllib2.URLError as exc:
            log.exception(exc)
            log.debug(
                "No internet connection detected. Checking again in 20 seconds."
            )
            time.sleep(20)


def generate_uuid():
    """Returns a random uuid as a string.

    Returns:
        (str): uuid generated from uuid4()
    """
    return str(uuid.uuid4())


class RepeatTimer(threading.Thread):
    """
    A helper class to create a repeating timer.
    threading.Timer is a one time deal.
    """
    def __init__(self, interval, callback, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interval = interval
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.event = threading.Event()
        self.event.set()

    def run(self):
        """Start the timer."""
        while self.event.is_set():
            thread = threading.Timer(
                self.interval, self.callback, self.args, self.kwargs
            )
            thread.daemon = True
            thread.start()
            thread.join()

    def stop(self):
        """Stop the timer."""
        self.event.clear()
