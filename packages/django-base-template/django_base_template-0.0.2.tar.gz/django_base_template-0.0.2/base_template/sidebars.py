from src.base_template.context_processors import get_menu_from_apps


def get_sidebar(request):
    if 'admin' in request.path:
        return get_menu_from_apps(request, 'admin')
    return get_menu_from_apps(request, 'site')


