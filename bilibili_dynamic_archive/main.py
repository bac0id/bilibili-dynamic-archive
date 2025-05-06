import asyncio
import sys

from dotenv import load_dotenv

from .archiver.archive_task_dispatcher import ArchiveTaskDispatcher
from .archiver.save_page_now_archiver import SavePageNowArchiver
from .bilibili_api.dynamic import Dynamic, ProxyDynamic
from .bilibili_api.user import Nemo2011BilibiliUser


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


def save_urls(urls: list):
    archiver = SavePageNowArchiver()
    dispatcher = ArchiveTaskDispatcher(archiver=archiver, urls=urls)
    dispatcher.start()


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
