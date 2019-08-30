from routes.aiohttp_rest import ApiAnswer

from handlers.base import Index, Login, Signup, Logout, PostView, Posts, Profile
from handlers.avatar import Avatar, Screen
from handlers.comments import CommentsView

from config.common import BaseConfig

class Router:

    web = None
    api = None

    def __init__(self, app, web, mediator, webSocket):
        self.web = web
        self.api = ApiAnswer()
        self.mediator = mediator
        self.TYPES = mediator.getEvents()
        self.TRIGGERS = mediator.getTriggers()
        routes = [
            # О юзерах
            ('GET', "/api/user", self.getUsers),  # Получить всех юзеров
            ('GET', "/api/user/{login}", self.getUser),  # Получить юзера по логину
            ('GET', "/api/user/type/{token}", self.getUserTypeByToken),  # Получить тип юзера по токену
            ('POST', "/api/user", self.register),  # Добавить юзера и студента одновременно
            ('GET', "/api/user/login/{login}/{password}/{rnd}", self.login),  # Логин юзера
            ('GET', "/api/user/logout/{token}", self.logout),  # Выход юзера
            # О группах
            ('GET', '/api/group/codes', self.getGroupsCodes),  # Получить коды групп
            # О студентах
            ('GET', '/api/student/note/{tokenAdmin}/{tokenStudent}', self.noteStudent),  # Отметить студентов
            ('GET', '/api/student/getOnLesson/{tokenAdmin}/{date}/{lessonNum}', self.getStudentsOnLesson)  # Получить список студентов, бывших на конкретной паре, конкретного дня
        ]

    def getUsers(self, request):
        return self.web.json_response(self.api.answer(self.mediator.get(self.TRIGGERS['GET_USERS'])))