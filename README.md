phenology-backend
=================

## Install
```bash
$ python boostrap.py -c buildout.cfg
$ ./bin/buildout -Nv
```

## Create database
```bash
$ ./bin/django_admin.py syncdb
$ ./bin/django_admin.py migrate --all
```

## Migration after each model changes
```
$ ./bin/django-admin.py schemamigration backend --auto
```

## Run Server
```bash
$ ./bin/django_admin.py runserver
```
