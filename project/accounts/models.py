from django.contrib.auth.models import User
from django.db import models


class Code(models.Model): # хранение кодов подтверждения почты
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="codes", )
    code = models.CharField(max_length=6)
