from dataclasses import dataclass
import requests
from requests import Response

from base.models import TgUser, Quiz, Answer, Question
from base.enums import UserState
from questionnaire.settings import QUERY_URL, QUIZ_ID


class BotManager:

    def __send_message(self, text: str, chat_id: int) -> Response:
        """
        Отправка сообщения
        :param text: Текст сообщения
        :param chat_id: ID чата
        """
        return requests.post(
            QUERY_URL + "sendMessage", json={"text": text, "chat_id": chat_id}
        )

    def __send_message_with_keyboard(
        self, question: Question, chat_id: int
    ) -> Response:
        """
        Отправка сообщения с клавиатурой
        :param question: Вопрос
        :param chat_id: ID чата
        """
        return requests.post(
            QUERY_URL + "sendMessage",
            json={
                "chat_id": chat_id,
                "text": question.text,
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": var.text, "callback_data": var.text}
                            for var in question.answer_variables.all()
                        ]
                    ]
                },
            },
        )

    def start_dialog(self, message: dict, callback=False):
        """
        Начало диалога
        :param message: Сообщение
        :param callback: Является ли это callback
        """
        user = self.__check_and_get_user(message)
        self.__greeting_and_first_question(user)
        self.__set_quiz(user)
        self.__set_question_and_send(user)
        return self.__handle_awnser(user, message, callback)

    def __greeting_and_first_question(self, user: TgUser):
        """
        Приветствие и первый вопрос
        :param user: Пользователь
        """
        if user.state == UserState.FIRST_TIME.value:
            self.__send_message(
                f"Привет, {user.first_name}.\n Сейчас я буду задавать вам вопросы.",
                user.chat_id,
            )

    def __check_and_get_user(self, message: dict):
        """
        Проверка и получение пользователя
        :param message: Сообщение
        :return: Пользователь
        """
        user_tg_id = message.get("from").get("id")
        if TgUser.objects.filter(tg_id=user_tg_id).count() == 0:
            tgUser = TgUser.objects.create(
                tg_id=message.get("from").get("id"),
                first_name=message.get("from").get("first_name"),
                last_name=message.get("from").get("last_name"),
                username=message.get("from").get("username"),
                chat_id=message.get("chat").get("id"),
            )
            return tgUser
        else:
            return TgUser.objects.get(tg_id=user_tg_id)

    def __set_quiz(self, user: TgUser):
        """
        Установка опроса
        :param user: Пользователь
        """
        id = QUIZ_ID
        if id is not None:
            quiz = Quiz.objects.get(id=id)
        else:
            quiz = Quiz.objects.order_by("?").first()
        user.quiz = quiz
        user.save()

    def __set_question_and_send(self, user: TgUser):
        """
        Установка вопроса и отправка
        :param user: Пользователь
        """
        question = user.question if user.question is not None else 0
        question_list = user.quiz.questions.filter(
            id__gt=question.id if not isinstance(question, int) else question
        )
        if question_list.count() != 0:
            user.question = question_list.first()
            if user.question.answer_variables.count() != 0:
                self.__send_message_with_keyboard(
                    question=user.question, chat_id=user.chat_id
                )
            else:
                self.__send_message(user.question.text, user.chat_id)

        elif user.state != UserState.FINISHED.value:
            user.state = UserState.LAST_QUESTION.value

        user.save()

    def __handle_awnser(self, user: TgUser, message: dict, callback: bool):
        """
        Обработка ответа пользователя
        :param user: Пользователь
        :param message: Сообщение
        :param callback: Является ли это callback
        """
        if user.state == UserState.FIRST_TIME.value:
            user.state = UserState.IN_QUIZ.value
            user.save()
            return {"sended": True}

        elif user.state == UserState.IN_QUIZ.value:
            if callback:
                Answer.objects.create(
                    text=message.get("data"), user=user, question=user.question
                )
            else:
                Answer.objects.create(
                    text=message.get("text"), user=user, question=user.question
                )
            return {"sended": True}

        elif user.state == UserState.LAST_QUESTION.value:
            if callback:
                Answer.objects.create(
                    text=message.get("data"), user=user, question=user.question
                )
            else:
                Answer.objects.create(
                    text=message.get("text"), user=user, question=user.question
                )
            self.__send_message("Спасибо что прошли опрос", user.chat_id)
            user.state = UserState.FINISHED.value
            user.save()
            return {"sended": True}

        elif user.state == UserState.FINISHED.value:
            self.__send_message("Вы уже прошли опрос :)", user.chat_id)
            return {"sended": True}
