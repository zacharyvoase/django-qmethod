# -*- coding: utf-8 -*-

import cPickle as pickle

from django.db import IntegrityError, models
from django.test import TestCase

from people.models import Group, Person


class SimpleTest(TestCase):

    fixtures = ['testing']

    def test_manager(self):
        self.failUnless(isinstance(
            Person.objects.minors(),
            models.query.QuerySet))

        self.failUnlessEqual(
            pks(Person.objects.minors()),
            pks(Person.objects.filter(age__lt=18)))

        self.failUnless(isinstance(
            Person.objects.adults(),
            models.query.QuerySet))

        self.failUnlessEqual(
            pks(Person.objects.adults()),
            pks(Person.objects.filter(age__gte=18)))

    def test_qset(self):
        self.failUnless(isinstance(
            Person.objects.all().minors(),
            models.query.QuerySet))

        self.failUnlessEqual(
            pks(Person.objects.all().minors()),
            pks(Person.objects.filter(age__lt=18)))

        self.failUnless(isinstance(
            Person.objects.all().adults(),
            models.query.QuerySet))

        self.failUnlessEqual(
            pks(Person.objects.all().adults()),
            pks(Person.objects.filter(age__gte=18)))


class RelationTest(TestCase):

    fixtures = ['testing']

    def test_querying(self):
        for group in Group.objects.all():
            self.failUnless(isinstance(
                group.people.all(),
                models.query.QuerySet))

            self.failUnless(isinstance(
                group.people.minors(),
                models.query.QuerySet))

            self.failUnlessEqual(
                pks(group.people.minors()),
                pks(group.people.filter(age__lt=18)))

            self.failUnless(isinstance(
                group.people.adults(),
                models.query.QuerySet))

            self.failUnlessEqual(
                pks(group.people.adults()),
                pks(group.people.filter(age__gte=18)))

    def test_creation(self):
        group = Group.objects.get(pk=1)
        person = group.people.create(age=32)
        assert person.group_id == group.pk

    def test_qmethods_get_the_original_object(self):
        group = Group.objects.get(pk=1)
        person, created = group.people.get_for_age(72)
        assert created
        assert person.age == 72
        assert person.group_id == group.pk

        # group_id cannot be NULL.
        with self.assertRaises(IntegrityError) as cm:
            Person.objects.get_for_age(22)
        assert "group_id" in cm.exception.message
        assert "NULL" in cm.exception.message


class PickleTest(TestCase):

    fixtures = ['testing']

    def assert_pickles(self, qset):
        self.failUnlessEqual(pks(qset),
                             pks(pickle.loads(pickle.dumps(qset))))

    def test(self):
        self.assert_pickles(Person.objects.minors())
        self.assert_pickles(Person.objects.all().minors())
        self.assert_pickles(Person.objects.minors().all())
        self.assert_pickles(Group.objects.all())
        self.assert_pickles(Group.objects.all()[0].people.all())
        self.assert_pickles(Group.objects.all()[0].people.minors())


def pks(qset):
    """Return the list of primary keys for the results of a QuerySet."""

    return sorted(tuple(qset.values_list('pk', flat=True)))
