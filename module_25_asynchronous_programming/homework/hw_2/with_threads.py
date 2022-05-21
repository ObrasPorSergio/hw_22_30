import threading
from pathlib import Path
import time
from typing import Any

import requests

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 100
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


def get_and_write_to_disk(url: str, id: int) -> None:
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        return
    print(response.status_code)
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode='wb') as f:
        f.write(response.content)


def get_cats_with_threads(number: int) -> Any:
    threads = []
    for i in range(number):
        thread = threading.Thread(target=get_and_write_to_disk, args=(URL, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    return threads


def main(number: int) -> None:
    res = get_cats_with_threads(number)
    print(len(res))


if __name__ == '__main__':
    start = time.time()
    main(10)
    print(f'Time for 10 with threads {time.time() - start}')

    start = time.time()
    main(50)
    print(f'Time for 50 with threads {time.time() - start}')

    start = time.time()
    main(100)
    print(f'Time for 100 with threads {time.time() - start}')
