# -*- coding: utf-8 -*-

__version__ = '0.0.2'

from functools import partial

from django.db import models


def attr_error(obj, attr):
    return AttributeError("%r object has no attribute %r" % (str(type(obj)), attr))


class QueryMethod(object):

    # Make querymethod objects a little cheaper.
    __slots__ = ('function',)

    def __init__(self, function):
        self.function = function

    def for_query_set(self, qset):
        return partial(self.function, qset)

querymethod = QueryMethod


class QMethodQuerySet(models.query.QuerySet):

    """A QuerySet which delegates to querymethods on its model."""

    def __getattr__(self, attr):
        qmethod = getattr(self.__dict__.get('model', None), attr, None)
        if isinstance(qmethod, QueryMethod):
            return qmethod.for_query_set(self)
        raise attr_error(self, attr)


class Manager(models.Manager):

    # If this is the default manager for a model, use this manager class for
    # relations (i.e. `group.people`, see README for details).
    use_for_related_fields = True

    def get_query_set(self, *args, **kwargs):
        return QMethodQuerySet(model=self.model, using=self._db)

    def __getattr__(self, attr):
        if not attr.startswith('_'):
            try:
                return getattr(self.get_query_set(), attr)
            except AttributeError:
                pass
        raise attr_error(self, attr)
