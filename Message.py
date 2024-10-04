from collections import defaultdict


class Message:
    def __init__(self, author: str, message: str):
        self.author: str = author
        self.message: str = message
        self.__reactions = defaultdict(set)
        self.__likes = set[str]()
        self.__dislikes = set[str]()
        self.__points: int = 0

    def get_likes(self) -> set:
        return self.__likes

    def get_dislikes(self) -> set:
        return self.__dislikes

    def get_reactions(self) -> defaultdict:
        return self.__reactions

    def get_points(self) -> int:
        return self.__points

    def reduce_points(self, decrease: int) -> None:
        self.__points -= decrease

    def add_point(self, increase: int) -> None:
        self.__points += increase