"""models for users app."""
from django.db import models


class TelegramUser(models.Model):
    """Model representing a Telegram user."""

    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    language_code = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        """Return a string representation of the TelegramUser instance."""
        return self.username or str(self.telegram_id)
