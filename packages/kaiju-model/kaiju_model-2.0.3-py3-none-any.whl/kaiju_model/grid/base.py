import abc

from kaiju_tools.services import Service

__all__ = ['BaseHandler']


class BaseHandler(Service, abc.ABC):

    def __init__(self, *args, locale, meta=None, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self._locale = locale
        self._meta = meta

    def call(self, *values):
        """May be sync or async."""
