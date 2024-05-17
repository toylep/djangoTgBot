from dataclasses import dataclass

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from base.models import Quiz, Answer, TgUser
from base.bot_reply import BotManager
import json


def start(request):
    """
    Start of tgbot
    :param request:
    :return: Простой ответ
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        is_callback = False
        if data.get("message"):
            message = data.get("message")
        else:
            message = data.get("callback_query")
            is_callback = True
        bot = BotManager()
        bot.start_dialog(message, callback=is_callback)

    return JsonResponse({"ok": True})


def admin(request):
    """
    Страничка типо для админа)))
    """
    awnsers = Answer.objects.all()
    return render(request, "admin.html", {"awnsers": awnsers})
