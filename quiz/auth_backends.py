from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class UUCMSIDAuthBackend(ModelBackend):
    def authenticate(self, request, uucms_id=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(uucms_id=uucms_id)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
