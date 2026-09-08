# yourapp/middleware.py

from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class ParticipantAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        cookies = {}

        # Parse cookies
        if b"cookie" in headers:
            cookie_header = headers[b"cookie"].decode()
            cookie_list = cookie_header.split("; ")
            for cookie in cookie_list:
                if "=" in cookie:
                    key, value = cookie.split("=", 1)
                    cookies[key] = value

        # Search for participant session cookie
        participant_cookie = None
        for key in cookies:
            if key.startswith("participant_sessionid_"):
                participant_cookie = cookies[key]
                break

        if participant_cookie:
            session = await self.get_session(participant_cookie)
            if session:
                user = await self.get_user(session)
                if user:
                    scope["user"] = user
                else:
                    scope["user"] = AnonymousUser()
            else:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_session(self, session_key):
        try:
            return Session.objects.get(session_key=session_key)
        except Session.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user(self, session):
        session_data = session.get_decoded()
        user_id = session_data.get("participant_user_id")
        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                return None
        return None
