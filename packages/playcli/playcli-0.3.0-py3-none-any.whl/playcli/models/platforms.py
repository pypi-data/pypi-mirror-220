from enum import Enum

from playcli.core import platforms as P
from playcli.models.driver import Driver


class Platforms(str, Enum):
    ALL = "all"
    RECURSIVE = "recursive"
    ELAMIGOS = "elamigos"
    STEAMUNLOCKED = "steamunlocked"

    def __iter__(self):
        for x in self.__class__._member_names_:
            if x in ["ALL", "RECURSIVE"]:
                continue

            yield self.dv(x)

    def find(self, id: str) -> tuple[str, Driver] | None:
        for driver in self.__iter__():
            platform: str = "-" + driver.__class__.__name__.lower()

            if id.endswith(platform):
                id_ = len(id) - len(platform)

                return (id[:id_], driver)

        return None

    def dv(self, ps: str = "") -> Driver:
        try:
            return getattr(P, ps.capitalize() if ps else self.value.capitalize())()
        except AttributeError:
            raise Exception(f"The '{self.value}' has no driver")
