from enum import Enum


class UserState(Enum):
    """
    Состояния пользователя
    """
    FIRST_TIME = 1
    IN_QUIZ = 2
    LAST_QUESTION = 3
    FINISHED = 4
