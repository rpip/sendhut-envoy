# from django.contrib.auth.models import AnonymousUser

registry = {}


def serialize(objects, user=None, serializer=None, *args, **kwargs):
    # if user is None:
    #     user = AnonymousUser()

    if not objects:
        return objects

    elif not isinstance(objects, (list, tuple, set, frozenset)):
        return serialize([objects], user=user, serializer=serializer, *args, **kwargs)[0]

    if serializer is None:
        # find the first object that is in the registry
        for o in objects:
            try:
                serializer = registry[type(o)]
                break
            except KeyError:
                pass
        else:
            return objects

    objects = [o for o in objects if o is not None]
    return [serializer(o, user=user, *args, **kwargs) for o in objects]


def register(type):
    def wrapped(cls):
        registry[type] = cls()
        return cls

    return wrapped


class Serializer(object):
    def __call__(self, obj, user, *args, **kwargs):
        if obj is None:
            return
        return self.serialize(obj, user, *args, **kwargs)

    def serialize(self, obj, user, *args, **kwargs):
        return {}
