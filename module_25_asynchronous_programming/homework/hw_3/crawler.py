import asyncio
import aiohttp
import aiofiles
from aiohttp import InvalidURL
from bs4 import BeautifulSoup


async def crawl(request_path, iteration) -> None:
    if iteration == 0:
        return

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(25)) as client:
        async with client.get(request_path) as response:
            result = await response.text()

            if request_path.startswith('http://'):
                request_path = request_path[7:]
            elif request_path.startswith('https://'):
                request_path = request_path[8:]
            elif request_path.startswith('http://www.'):
                request_path = request_path[11:]
            elif request_path.startswith('https://www.'):
                request_path = request_path[12:]

            soup = BeautifulSoup(result, 'html.parser')

            for link in soup.find_all('a'):
                data = link.get('href')
                try:
                    if data.startswith(('http://', 'https://')) and request_path not in data:
                        await write_to_disk(data, iteration)
                        await crawl(data, iteration-1)
                except (TypeError, AttributeError, InvalidURL) as err:
                    print(err)
                    pass


async def write_to_disk(content, level):
    async with aiofiles.open('parsed_links.log', 'a', encoding='utf8') as f:
        await f.write(f'{content} - {level}\n')


def main(request_path, depth=3):
    asyncio.run(crawl(request_path, iteration=depth))


if __name__ == '__main__':
    path = input('Input path, starting with http:// or https://: ')
    iteration_depth = int(input('Input depth level(int): '))

    main(path, iteration_depth)
