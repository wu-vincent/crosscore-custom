import argparse
import asyncio
import logging
import os
import shutil
import tempfile

import aiohttp
import tqdm.asyncio
import tqdm.contrib.logging

base_url = "https://cdn.megagamelog.com/cross/release/{platform}/curr_1/Custom/"
logger = logging.getLogger(__name__)


async def download_file(session, url, path):
    async with session.get(url) as response:
        if response.status == 200:  # Check if the response is OK
            with open(path, 'wb') as f:
                f.write(await response.read())
        else:
            logger.warning(f"Skipping {url}, received status code: {response.status}")


async def main(platform: str):
    assert platform in ["android", "ios"]

    with open("ilist.txt", "r", encoding='utf-8-sig') as file:
        items = file.read().split(',')

    with tempfile.TemporaryDirectory() as temp_dir:
        with tqdm.contrib.logging.logging_redirect_tqdm():
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
