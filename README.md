# Django Comment

## Installation

~~~
> pipenv install https://github.com/genosltd/django-comment
~~~

## Usage

Do not forget to list `django_comment` in `settings.py`:

~~~python
# settings.py
INSTALLED_APPS = [
    'django_comment',
]
~~~

### Models

~~~python
# models.py
from django_comment.models import HasComments

class AModel(HasComments):
    pass
~~~

~~~
>>> from django.auth.models import User
>>> from models import AModel
>>> user = User.objects.get(username='user')
>>> a_model = AModel.objects.create()
>>> a_model.comments.create(author=user, comment='This is a comment')

~~~

### Admin

~~~python
# admin.py
from django.contrib import admin
from django_comment.admin import HasCommentsAdmin

from . import models

@admin.register(models.AModel)
class AModelAdmin(HasCommentsAdmin):
    pass
~~~

