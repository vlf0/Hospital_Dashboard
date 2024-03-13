from django.contrib.auth.models import AbstractUser


# Override default user's class for easy extensions
class CustomUser(AbstractUser):
    pass
