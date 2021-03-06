from enum import Enum


class UseCase(Enum):
    UNKNOWN = 0
    CUSTOM = 1
    SEARCH = 2
    SEARCH_SUGGESTIONS = 3
    FEED = 4
    RELATED_CONTENT = 5
    CLOSE_UP = 6
    CATEGORY_CONTENT = 7
    MY_CONTENT = 8
    MY_SAVED_CONTENT = 9
    SELLER_CONTENT = 10
    DISCOVER = 11
