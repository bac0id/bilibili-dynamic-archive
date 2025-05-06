import time

from .archiver import Archiver


class ArchiveTaskDispatcher:
    def __init__(self, archiver: Archiver, urls: list):

        self.archiver = archiver
        self.urls = urls

    def start(self):
        self.__save_urls(self.urls)

    def __save_url(self, url) -> bool:
        is_successfully_saved = False
        try:
            is_successfully_saved = self.archiver.save(url)
        except Exception as e:
            print(e)
        return is_successfully_saved

    def __save_urls(self, urls):
        while len(urls) > 0:
            failed_urls = []

            for url in urls:
                print(f"Saving {url}")
                is_successfully_saved = self.__save_url(url)
                if is_successfully_saved:
                    print(f"Saved")
                else:
                    print(f"Failed")
                    failed_urls.append(url)
                time.sleep(4)

            print(f"Count of failed urls: {len(failed_urls)}")
            print(f"Failed urls: {failed_urls}")
            time.sleep(4)

            urls = failed_urls
        return failed_urls
