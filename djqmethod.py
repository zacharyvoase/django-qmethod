# -*- coding: utf-8 -*-

__version__ = '0.0.3'

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


class QMethodLookupMixin(object):
    """Delegate missing attributes to querymethods on ``self.model``."""

    def __getattr__(self, attr):
        # Using `object.__getattribute__` avoids infinite loops if the 'model'
        # attribute does not exist.
        qmethod = getattr(object.__getattribute__(self, 'model'), attr, None)
        if isinstance(qmethod, QueryMethod):
            return qmethod.for_query_set(self)
        raise attr_error(self, attr)


class QMethodQuerySet(models.query.QuerySet, QMethodLookupMixin):
    pass


class Manager(models.Manager, QMethodLookupMixin):

    # If this is the default manager for a model, use this manager class for
    # relations (i.e. `group.people`, see README for details).
    use_for_related_fields = True

    def get_query_set(self, *args, **kwargs):
        return QMethodQuerySet(model=self.model, using=self._db)
