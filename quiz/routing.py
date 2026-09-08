from django.urls import re_path
from . import consumers
from quiz import consumers

websocket_urlpatterns = [
    re_path(r'ws/participant/$', consumers.ParticipantConsumer.as_asgi()),
    re_path(r'ws/admin/$', consumers.AdminConsumer.as_asgi()),
]
