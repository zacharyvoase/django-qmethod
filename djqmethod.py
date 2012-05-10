# -*- coding: utf-8 -*-

__version__ = '0.0.1'

from functools import partial

from django.db import models


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
        if hasattr(self.__dict__.get('model', None), attr):
            qmethod = getattr(self.model, attr)
            if isinstance(qmethod, QueryMethod):
                return qmethod.for_query_set(self)
        return super(QMethodQuerySet, self).__getattr__(attr)


class Manager(models.Manager):

    # If this is the default manager for a model, use this manager class for
    # relations (i.e. `group.people`, see README for details).
    use_for_related_fields = True

    def get_query_set(self, *args, **kwargs):
        return QMethodQuerySet(model=self.model)

    def __getattr__(self, attr):
        return getattr(self.get_query_set(), attr)
