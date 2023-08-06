from functools import wraps


def is_logged_check(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.is_logged:
            raise Exception("You must be logged in to use this method")
        return method(self, *args, **kwargs)

    return wrapper
