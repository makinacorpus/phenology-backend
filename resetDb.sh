#!/bin/sh 
./bin/django-admin.py sqlclear backend auth| ./bin/django-admin.py dbshell;
./bin/django-admin.py syncdb --noinput;
#echo "from django.contrib.auth.models import UserManager; UserManager().create_superuser('admin', 'myemail@example.com', 'admin', [])" | ./bin/django-admin.py shell
./bin/django-admin.py runscript resetDb;
