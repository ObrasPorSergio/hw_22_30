import random

import requests
import time


def run():
    while True:
        try:
            requests.get("http://app:5000/connection", timeout=1)
            time.sleep(random.randint(1, 5) / 50)
        except:
            pass


if __name__ == '__main__':
    run()