from django.apps import apps

from src.base_template.utils import get_class_from_settings, get_settings_value


def get_menu_from_apps(request, menu):
    menu = "get_{}_sidebar".format(menu)
    all_apps_conf = apps.get_app_configs()
    sidebar_list = []
    for app_conf in all_apps_conf:
        if hasattr(app_conf, menu) and callable(getattr(app_conf, menu)):
            items = getattr(app_conf, menu)(request)
            if type(items) == list:
                sidebar_list = sidebar_list + items
            else:
                sidebar_list.append(items)
    sidebar_list = sorted(sidebar_list, key=lambda d: d['order'])
    return sidebar_list


def get_sidebar(request):
    sidebar = get_class_from_settings("BASE_TEMPLATE_GET_SIDEBAR_METHOD")(request)
    allowed_sidebar = []
    for item in sidebar:
        if item['permissions']:
            if 'children' in item and len(item['children']) > 0:
                allowed_items = []
                for sub_item in item['children']:
                    allowed_items.append(sub_item)
                item['children'] = allowed_items
        allowed_sidebar.append(item)

    return allowed_sidebar


def base_template(request):
    return {
        "multiple_languages": get_settings_value("BASE_TEMPLATE_MULTIPLE_LANGUAGES", False),

        "sidebar": {
            "menu": get_sidebar(request),
            "logo": get_settings_value("BASE_TEMPLATE_SIDEBAR_LOGO", None),
            "logo_icon": get_settings_value("BASE_TEMPLATE_SIDEBAR_LOGO_ICON", None),
            "footer": get_settings_value("BASE_TEMPLATE_SIDEBAR_FOOTER_TEMPLATE", None),
        },
        "header": {
            "logo": get_settings_value("BASE_TEMPLATE_HEADER_LOGO", None),
            "right_menus": get_settings_value("BASE_TEMPLATE_HEADER_RIGHT_MENUS", None),
            "left_menus": get_settings_value("BASE_TEMPLATE_HEADER_LEFT_MENUS", None),
        },
        "footer": {
            "links_template_name": get_settings_value("BASE_TEMPLATE_LINKS_TEMPLATE", None),
            "copyrights": get_settings_value("BASE_TEMPLATE_COPYRIGHTS", None),
        }
    }
