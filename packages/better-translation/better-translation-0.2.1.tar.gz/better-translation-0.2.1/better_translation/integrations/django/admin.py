from __future__ import annotations

from django import forms
from django.contrib import admin
from django.db import models

from better_translation.integrations.django.models import (
    BaseMessage,
    BaseTranslation,
)

admin.ModelAdmin.__class_getitem__ = classmethod(  # type: ignore[attr-defined]
    lambda cls, _: cls,
)
admin.TabularInline.__class_getitem__ = classmethod(  # type: ignore[attr-defined]
    lambda cls, _: cls,
)


class BaseMessageAdmin(admin.ModelAdmin[BaseMessage]):
    list_display = ("id", "default", "default_plural", "is_used")
    readonly_fields = list_display
    search_fields = (
        "id",
        "default",
        "default_plural",
        "translations__singular",
        "translations__plural",
    )


class BaseTranslationInline(admin.TabularInline[BaseTranslation]):
    extra = 0
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"rows": 6, "cols": 50}),
        },
    }
