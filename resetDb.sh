#!/bin/sh 
./bin/django-admin.py sqlclear backend | ./bin/django-admin.py dbshell;
./bin/django-admin.py syncdb;
./bin/django-admin.py runscript resetDb;
