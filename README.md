# `django-qmethod`

`django-qmethod` is a library for easily defining operations on collections of
Django models (that is, QuerySets and Managers).

One day, I hope something like this is included in Django core.


## Usage

Basic usage is as follows:

```python
import cPickle as pickle
from django.db import models
from djqmethod import Manager, querymethod

class Group(models.Model):
    pass

class Person(models.Model):
    GENDERS = dict(m='Male', f='Female', u='Unspecified').items()

    group = models.ForeignKey(Group, related_name='people')
    gender = models.CharField(max_length=1, choices=GENDERS)
    age = models.PositiveIntegerField()

    # Note: you need to create an explicit manager here.
    objects = Manager()

    @querymethod
    def minors(query):
        return query.filter(age__lt=18)

    @querymethod
    def adults(query):
        return query.filter(age__gte=18)

# The `minors()` and `adults()` methods will be available on the manager:
assert isinstance(Person.objects.minors(), models.query.QuerySet)

# They'll be available on subsequent querysets:
assert isinstance(Person.objects.filter(gender='m').minors(),
                  models.query.QuerySet)

# They'll also be available on relations, if they were mixed in to the
# default manager for that model:
group = Group.objects.all()[0]
assert isinstance(group.people.minors(), models.query.QuerySet)

# The QuerySets produced are totally pickle-safe:
assert isinstance(pickle.loads(pickle.dumps(Person.objects.minors())),
                  models.query.QuerySet)
```

A test project is located in `test/example/`; consult this for a more
comprehensive example.


## Installation

    pip install django-qmethod


## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
