#!/bin/bash
echo '=================Project Data Tracker Setup=============='
echo 'Creating Database...'
python manage.py makemigrations 
python manage.py migrate
echo 'Create a super user:'
python manage.py createsuperuser
echo 'Done. Enjoy it!'

