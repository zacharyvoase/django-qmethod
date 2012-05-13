# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from djqmethod import Manager, querymethod


class SiteManager(CurrentSiteManager, Manager):
    pass


class Group(models.Model):
    pass


class Person(models.Model):

    group = models.ForeignKey(Group, related_name='people')
    age = models.PositiveIntegerField()
    site = models.ForeignKey(Site, related_name='people', null=True)

    objects = Manager()
    on_site = SiteManager()

    @querymethod
    def minors(query):
        return query.filter(age__lt=18)

    @querymethod
    def adults(query):
        return query.filter(age__gte=18)

    @querymethod
    def get_for_age(query, age):
        return query.get_or_create(age=age)
