OMERO.qa
========

OMERO.qa is the web application which helps support community by OMERO team.

Requirements
============

* PostgreSQL 9.1+
* Python 2.7+

Development Installation
========================

1. Clone the repository

        git clone git@github.com:openmicroscopy/registry.git

2. Set up a virtualenv (http://www.pip-installer.org/) and activate it

        curl -O -k https://raw.github.com/pypa/virtualenv/master/virtualenv.py
        python virtualenv.py reg-virtualenv
        source reg-virtualenv/bin/activate
        pip install numpy
        pip install -r requirements.txt

3. Download and extract GeoIP databases

        GeoIP2-Domain.mmdb, GeoIPOrg.dat, GeoLite2-City.mmdb

4. Run tests

        python manage.py test --settings=omeroregistry.settings-test -v 3

Configuration
=============

* Create new settings-prod.py and import default settings

        from settings import *

* Set `DEBUG`

        DEBUG=False
        TEMPLATE_DEBUG = DEBUG

* Set `ADMINS`

        ADMINS = (
            ('Full Name', 'email@example.com'),
        )

* Change database settings

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                                                # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'stats_database',       # Or path to database file if using sqlite3.
                'USER': 'stats_user',           # Not used with sqlite3.
                'PASSWORD': 'secret',           # Not used with sqlite3.
                'HOST': 'localhost',            # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '5432',                 # Set to empty string for default. Not used with sqlite3.
            }
        }

* Set up email server
    
        # Application allows to notify user
        EMAIL_HOST = 'localhost'
        EMAIL_HOST_PASSWORD = ''
        EMAIL_HOST_USER = ''
        EMAIL_PORT = 25
        EMAIL_SUBJECT_PREFIX = '[OMERO.stats] '
        EMAIL_USE_TLS = False
        SERVER_EMAIL = 'email@example.com' # email address

* Synchronise the database

        export DJANGO_SETTINGS_MODULE=omeroregistry.settings-prod
        python manage.py syncdb

        # upgrade DB if needed
        python manage.py sqlcustom registry | python manage.py dbshell


Deployment
==========

* Nginx

    * Deploy using apache template

* Apache

    * Update paths in omeroregistry/django.wsgi
    * Deploy using apache template

Legal
=====

The source for OMERO.registry is released under the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OMERO.registry is Copyright (C) 2015 University of Dundee
