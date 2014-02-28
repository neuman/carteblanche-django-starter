carteblanche-django-starter
===============================

CarteBlanche Django Starter App

Installation
------------

make sure you have pip and bower installed on your system

pip install -r requirements.txt

bower install

python manage.py syncdb
python manage.py schemamigration --auto core
python manage.py migrate

python manage.py runserver 0.0.0.0:2222

