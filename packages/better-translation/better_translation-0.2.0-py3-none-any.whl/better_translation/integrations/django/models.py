from __future__ import annotations

from typing import cast

try:
    from django.db import models
except ImportError as e:
    msg = "Django is not installed. To use Django integration, install Django."
    raise ValueError(msg) from e


class DefaultLocalesChoices(models.TextChoices):
    RU = "ru", "Russian"
    EN = "en", "English"


class BaseMessage(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    default = models.TextField(
        verbose_name="Default singular form of the message",
    )
    default_plural = models.TextField(
        verbose_name="Default plural form of the message",
    )
    is_used = models.BooleanField(verbose_name="Is used", default=True)

    translations: models.QuerySet[BaseTranslation]
    """A QuerySet of translations for this message."""

    def __str__(self) -> str:
        return f"Message: {self.id}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseMessage):
            return False

        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    class _Meta:
        abstract = True

    Meta = cast("type[models.Model.Meta]", _Meta)


class BaseTranslation(models.Model):
    locale = models.CharField(
        max_length=5,
        verbose_name="Locale",
        choices=DefaultLocalesChoices.choices,
    )
    singular = models.TextField(verbose_name="Singular form of the text")
    plural = models.TextField(
        verbose_name="Plural form of the text",
        default="",
        blank=True,
    )

    message = models.ForeignKey(
        BaseMessage,
        on_delete=models.CASCADE,
        related_name="translations",
    )

    def __str__(self) -> str:
        return f"MessageTranslation('{self.locale}', '{self.singular[:10]}...')"

    class _Meta:
        abstract = True

    Meta = cast("type[models.Model.Meta]", _Meta)
