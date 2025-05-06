import asyncio
import sys
import time
from collections import deque

from dotenv import load_dotenv

from bilibili_dynamic_archive.archiver.save_page_now_archiver import (
    SavePageNowArchiver,
)
from bilibili_dynamic_archive.bilibili_api.dynamic import Dynamic, ProxyDynamic
from bilibili_dynamic_archive.bilibili_api.user import Nemo2011BilibiliUser


async def get_dynamics(uid) -> list[Dynamic]:
    user = Nemo2011BilibiliUser(uid=uid)
    dynamics_json_objs = await user.get_all_dynamics()
    dynamics = [ProxyDynamic(json_obj) for json_obj in dynamics_json_objs]
    return dynamics


def get_urls_to_save(dynamics: list[Dynamic]) -> list[str]:
    all_urls = set()

    for dynamic in dynamics:
        dynamic_url = dynamic.get_url()
        all_urls.add(dynamic_url)

        resource_urls = dynamic.get_resources_urls()
        for url in resource_urls:
            all_urls.add(url)

    return list(all_urls)


def save_url(url, archiver) -> bool:
    is_successfully_saved = False
    try:
        is_successfully_saved = archiver.save(url)
    except Exception as e:
        print(e)
    return is_successfully_saved


def save_urls(urls) -> list:
    archiver = SavePageNowArchiver()
    while len(urls) > 0:
        failed_urls = []

        for url in urls:
            print(f"Saving {url}")
            is_successfully_saved = save_url(url, archiver)
            if is_successfully_saved:
                print(f"Saved {url}")
            else:
                print(f"Failed {url}")
                failed_urls.append(url)
            time.sleep(4)

        print(f"Count of failed urls: {len(failed_urls)}")
        print(f"Failed urls: {failed_urls}")
        time.sleep(4)

        urls = failed_urls
    return failed_urls


def save_urls_recycle(urls):
    archiver = SavePageNowArchiver()
    urls = deque(urls)
    while len(urls) > 0:
        url = urls.popleft()
        is_successfully_saved = save_url(url, archiver)
        if is_successfully_saved:
            print(f"Saved")
        else:
            print(f"Failed")
            urls.append(url)


def parse_argument():
    if len(sys.argv) < 2:
        print("""Usage: bili-archive <uid>""")
        sys.exit(1)

    try:
        uid = int(sys.argv[1])
    except ValueError:
        print(
            f"Error: Invalid UID provided. '{sys.argv[1]}' is not an integer."
        )
        sys.exit(1)
    return uid


async def main_async():
    load_dotenv()

    uid = parse_argument()
    print(f"Uid: {uid}")

    dynamics = await get_dynamics(uid)
    print(f"Cound of dynamics: {len(dynamics)}")

    urls_to_save = get_urls_to_save(dynamics)
    print(f"Cound of urls: {len(urls_to_save)}")
    print(f"Urls:{urls_to_save}")

    save_urls(urls_to_save)


def main():
    try:
        asyncio.run(main_async())
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
