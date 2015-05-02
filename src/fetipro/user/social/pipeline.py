# encoding=utf-8


def save_display_name(backend, user, is_new, details, *args, **kwargs):
        user.display_name = details.get("fullname")
        user.email = details.get("email")
        user.save()
