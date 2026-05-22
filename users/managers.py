from django.contrib.auth.models import BaseUserManager

from team_finder.constants import USER_PHONE_MAX_LENGTH
from users.avatar import build_avatar_file


class UserManager(BaseUserManager):
    def _assign_avatar(self, user):
        if not user.avatar:
            user.avatar.save(
                f"user_{user.email}.png",
                build_avatar_file(user.name),
                save=False,
            )

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if not user.phone:
            suffix = abs(hash(email)) % 10_000_000_000
            user.phone = f"+7{suffix:010d}"[:USER_PHONE_MAX_LENGTH]
        user.set_password(password)
        self._assign_avatar(user)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("name", "Admin")
        extra_fields.setdefault("surname", "User")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
