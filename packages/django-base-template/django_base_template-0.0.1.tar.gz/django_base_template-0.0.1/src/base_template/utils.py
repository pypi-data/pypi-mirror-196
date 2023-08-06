import importlib

from django.conf import settings


def get_settings_value(settings_key, default_value=None):
    return getattr(settings, settings_key, default_value)


def import_class_or_function(name):
    name_split = name.split('.')
    name = name_split[-1:][0]
    module_name = name_split[:-1]
    return getattr(importlib.import_module('.'.join(module_name)), name)


def get_class_from_settings(settings_key, default_class=None):
    class_name = get_settings_value(settings_key, None)

    if not class_name:
        class_name = default_class

    return import_class_or_function(class_name) if type(class_name) is str else class_name
