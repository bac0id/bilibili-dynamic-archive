import abc
import os


class Archiver(abc.ABC):
    @abc.abstractmethod
    def save(self, url: str) -> bool:
        """
        Save a url.
        Args:
            url (str): Url to save
        Returns:
            bool: Is successfully saved?
        """
        pass
