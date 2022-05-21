import asyncio
import contextvars
import functools
from pathlib import Path
import time
from typing import Any

import aiohttp

URL = 'https://cataas.com/cat'
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)


async def get_cat(client: aiohttp.ClientSession, idx: int) -> None:
    async with client.get(URL) as response:
        print(response.status)
        result = await response.read()
        await asyncio.gather(to_thread(write_to_disk, result, idx))


def write_to_disk(content: bytes, id: int) -> None:
    file_path = "{}/{}.png".format(OUT_PATH, id)
    with open(file_path, mode='wb') as f:
        f.write(content)


async def get_all_cats(number: int) -> Any:
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(number)]
        return await asyncio.gather(*tasks)


def main(number: int) -> None:
    res = asyncio.run(get_all_cats(number))
    print(len(res))


if __name__ == '__main__':
    start = time.time()
    main(10)
    print(f'Time for 10 without aiofiles {time.time() - start}')

    start = time.time()
    main(50)
    print(f'Time for 50 without aiofiles {time.time() - start}')

    start = time.time()
    main(100)
    print(f'Time for 100 without aiofiles {time.time() - start}')
