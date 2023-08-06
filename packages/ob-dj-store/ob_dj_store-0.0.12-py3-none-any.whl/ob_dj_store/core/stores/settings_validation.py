from django.apps import apps
from django.core.checks import Error
from django.utils.module_loading import import_string

from config import settings

REQUIRED_INSTALLED_APPS = [
    "rest_framework",
]


def required_installed_apps(app_configs, **kwargs):
    return [
        Error(f"{app} is required in INSTALLED_APPS")
        for app in REQUIRED_INSTALLED_APPS
        if not apps.is_installed(app)
    ]


def store_validation_settings(app_configs, **kwargs):
    errors = []
    if getattr(settings, "GIFT", None) and not getattr(
        settings, "GIFT_PAYMENT_METHOD_PATH", None
    ):
        errors.append(
            Error(
                "GIFT_PAYMENT_METHOD_PATH must be set if GIFT is in Payment methods",
                id="store_validation_settings_error",
            )
        )

    def _path_validation(path):
        try:
            print(path)
            path_class = import_string(path)
        except ImportError:
            errors.append(
                Error(
                    f"{path} is not a valid path", id="store_validation_settings_error"
                )
            )

    if getattr(settings, "GIFT_PAYMENT_METHOD_PATH", None):
        _path_validation(settings.GIFT_PAYMENT_METHOD_PATH)
    return errors
