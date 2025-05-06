import abc

from bilibili_api.user import User


class BilibiliUser(abc.ABC):
    def __init__(self, uid: int):
        self.uid = uid

    @abc.abstractmethod
    async def get_all_dynamics(self) -> list:
        pass


class Nemo2011BilibiliUser(BilibiliUser):
    def __init__(self, uid: int):
        super().__init__(uid)
        self.user = User(uid=uid)

    async def get_all_dynamics(self):
        offset = ""
        dynamics = []
        while True:
            page = await self.user.get_dynamics_new(offset)
            dynamics.extend(page["items"])
            if page["has_more"] != 1:
                break
            offset = page["offset"]
        return dynamics
