from typing import List, Optional, Iterable

from aiohttp.web_app import Application


class Store:
    """
    Store collection
    """

    def __init__(self):
        self.words: set = set()

    def add(self, words: Iterable[str]):
        """
        Add new word in storage, if word already in storage then nothing will happen
        :param words: list of words
        :return: None
        """
        for word in words:
            self.words.add(word)

    def get_anagrams(self, word: str) -> Optional[List[str]]:
        """
        Get list of anagrams by word
        :param word: word string
        :return: None or list of anagrams
        """
        word = sorted(word.lower())
        anagrams = list(filter(lambda x: sorted(x) == word, self.words))
        return anagrams or None


async def init_store(app: Application):
    app['store'] = Store()
