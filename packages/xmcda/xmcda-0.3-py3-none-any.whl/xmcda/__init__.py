import threading
from collections import namedtuple

from . import schemas

# -- Selecting which version should be used
_local = threading.local()

_local.version = schemas.XMCDA_4_0_0


def version():
    return _local.version


def set_version(version):
    _local.version = version


def reset_version():
    _local.version = schemas.XMCDA_4_0_0


class NotSupportedVersionError(NotImplementedError):  # pragma: no cover
    def __init__(self, version):
        super().__init__(f"Unsupported XMCDA version {version}")


# --
settings = threading.local()


TagInfo = namedtuple('TagInfo',
                     ('tag', 'attribute', 'klass', 'contained_class'))


def set_export_defaults(include_defaults):
    settings.xmcda_export_defaults = include_defaults


def export_defaults():
    return getattr(settings, 'xmcda_export_defaults', False)


__create_default = True


def set_create_on_access(create_on_access, tag=None):
    settings.create_on_access = getattr(settings, 'create_on_access', {})
    if type(tag) is type:
        tag = camel_to_snake(tag.__name__)
    settings.create_on_access[tag] = create_on_access


def camel_to_snake(class_name):
    '''Converts a class name to snake case. The function expects that the
    string 'class_name' starts with a capital letter.
    '''
    return ''.join('_'+c.lower() if c <= 'Z' else c for c in class_name)[1:]


def create_on_access(tag=None):
    d = getattr(settings, 'create_on_access', None)
    if d is None:
        return __create_default
    if type(tag) is type:
        tag = camel_to_snake(tag.__name__)
    # if nothing is set for the tag, return the default settings
    return d.get(tag, d.get(None, __create_default))


def reset_settings():
    for attribute in ('xmcda_export_defaults', 'create_on_access'):
        try:
            delattr(settings, attribute)
        except AttributeError:
            pass


# -- marking instances on creation
_creation_marker = threading.local()


def set_creation_marker(marker):
    _creation_marker.marker = marker


def creation_marker():
    if not hasattr(_creation_marker, 'marker'):
        _creation_marker.marker = None
    return _creation_marker.marker


def mark_creation(klass, attrname='marker'):
    if hasattr(klass, attrname):
        raise ValueError(f'Class {klass} already defines {attrname}')
    init = klass.__init__

    def decorated_init(self, *args, **kw):
        self.marker = creation_marker()
        init(self, *args, **kw)

    klass.__init__ = decorated_init
    return klass


class ValidationError(Exception):
    pass
