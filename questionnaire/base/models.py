from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    """
    Опрос
    """

    name = models.CharField(max_length=100)


class Question(models.Model):
    """
    Вопрос
    """

    text = models.TextField()
    quiz = models.ForeignKey(
        to=Quiz, related_name="questions", on_delete=models.CASCADE
    )


class AnswerVariable(models.Model):
    """
    Вариант ответа
    """

    text = models.TextField()
    question = models.ForeignKey(
        to=Question,
        related_name="answer_variables",
        on_delete=models.CASCADE,
    )


class TgUser(models.Model):
    """
    Tg пользователь
    """

    tg_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50)
    chat_id = models.IntegerField(unique=True)
    question = models.ForeignKey(to=Question, null=True, on_delete=models.CASCADE)
    quiz = models.ForeignKey(to=Quiz, null=True, on_delete=models.CASCADE)
    state = models.IntegerField(default=1)


class Answer(models.Model):
    """
    Ответ пользователя
    """

    text = models.TextField()
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
