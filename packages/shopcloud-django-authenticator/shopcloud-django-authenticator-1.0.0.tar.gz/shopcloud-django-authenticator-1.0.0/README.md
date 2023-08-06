# Shopcloud-Django-Authenticator

Single Sign In from Shopcloud

## Quickstart

```
pip3 istall shopcloud-django-authenticator
```

1. Add "authenticator" to your INSTALLED_APPS setting like this::

```py
INSTALLED_APPS = [
    ...
    'authenticator',
]
```

2. Include the polls URLconf in your project urls.py like this::

```
path('authenticator/', include('monitoring.urls')),
```

3. Run `python manage.py migrate` to create the polls models.


## Release

```sh
$ rm -rf build dist
$ pip3 install wheel twine
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/*
```
