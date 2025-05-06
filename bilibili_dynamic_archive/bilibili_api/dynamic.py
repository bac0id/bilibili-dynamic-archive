import abc


class Dynamic(abc.ABC):
    @abc.abstractmethod
    def get_id(self) -> str:
        pass

    @abc.abstractmethod
    def get_url(self) -> str:
        pass

    @abc.abstractmethod
    def get_resources_urls(self) -> list[str]:
        pass

    @abc.abstractmethod
    def has_forwarded_dynamic(self) -> bool:
        pass


class ProxyDynamic(Dynamic):
    def __init__(self, json):
        super().__init__()
        self.json = json

    def get_id(self) -> str:
        id_str = self.json["id_str"]
        return id_str

    def get_url(self) -> str:
        id = self.get_id()
        url = f"https://www.bilibili.com/opus/{id}"
        return url

    def get_forwarded_dynamic_json(self):
        if not self.has_forwarded_dynamic():
            return None
        return self.json["orig"]

    def has_forwarded_dynamic(self) -> bool:
        return "orig" in self.json

    def get_resources_urls(self) -> list[str]:
        resources_urls = []

        if not self.has_forwarded_dynamic():
            module_dynamic = self.json["modules"]["module_dynamic"]
            major = module_dynamic["major"]
            urls = ProxyDynamic.__get_resources_urls_from_major(major)
            resources_urls.extend(urls)
        else:
            forwarded_dynamic = ProxyDynamic(self.get_forwarded_dynamic_json())
            resources_urls_of_forwarded_dynamic = (
                forwarded_dynamic.get_resources_urls()
            )
            resources_urls.extend(resources_urls_of_forwarded_dynamic)

        return resources_urls

    @staticmethod
    def __get_resources_urls_from_major(major):
        resources_urls = []

        if "opus" in major:
            opus = major["opus"]
            urls = ProxyDynamic.__get_resources_urls_from_opus(opus)
            resources_urls.extend(urls)

        if "archive" in major:
            archive = major["archive"]
            urls = ProxyDynamic.__get_resources_urls_from_archive(archive)
            resources_urls.extend(urls)

        return resources_urls

    @staticmethod
    def __get_resources_urls_from_opus(opus):
        resources_urls = []

        pics = opus["pics"]
        for pic in pics:
            url = pic["url"]
            resources_urls.append(url)

        return resources_urls

    @staticmethod
    def __get_resources_urls_from_archive(archive):
        resources_urls = []

        # video page
        # example: "BVxxyy123"
        bvid = archive["bvid"]
        video_url = f"https://www.bilibili.com/video/{bvid}/"
        resources_urls.append(video_url)

        # video cover
        # example: "http://i0.hdslb.com/bfs/archive/1c72a5b6e82586196e302f4b5d807bfddb8b31e4.png"
        cover = archive["cover"]
        resources_urls.append(cover)

        return resources_urls
