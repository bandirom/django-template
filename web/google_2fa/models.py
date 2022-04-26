from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

User.add_to_class('enable_2fa', models.BooleanField(default=False))
