import os
import argparse
import shutil
import tempfile
import aiohttp
import asyncio
import tqdm.asyncio

base_url = "https://cdn.megagamelog.com/cross/release/{platform}/curr_1/Custom/"


async def download_file(session, url, path):
    async with session.get(url) as response:
        with open(path, 'wb') as f:
            f.write(await response.read())


async def main(platform: str):
    assert platform in ["android", "ios"]

    with open("ilist.txt", "r", encoding='utf-8-sig') as file:
        items = file.read().split(',')

    with tempfile.TemporaryDirectory() as temp_dir:
        custom_dir = os.path.join(temp_dir, 'Custom')
        os.makedirs(custom_dir, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            tasks = []
            for item in items:
                url = base_url.format(platform=platform) + item
                path = os.path.join(custom_dir, item)
                tasks.append(download_file(session, url, path))

            for f in tqdm.asyncio.tqdm.as_completed(tasks):
                await f

        shutil.make_archive('custom-{}'.format(platform), 'zip', temp_dir, 'Custom')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", help="Specify the platform (android or ios)")
    args = parser.parse_args()

    asyncio.run(main(args.platform))
