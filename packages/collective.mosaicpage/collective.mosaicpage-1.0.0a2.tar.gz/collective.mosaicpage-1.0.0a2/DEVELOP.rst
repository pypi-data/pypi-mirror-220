Using the development buildout
==============================

plonecli
--------

The convenient way, use plonecli build ;)::

    $ plonecli build

or with --clear if you want to clean your existing venv::

    $ plonecli build --clear

Start your instance::

    $ plonecli serve


Without plonecli
----------------

Create a virtualenv in the package::

    $ python3 -m venv venv

or with --clear if you want to clean your existing venv::

    $ python3 -m venv venv --clear

Install requirements with pip::

    $ ./venv/bin/pip install -r requirements.txt

bootstrap your buildout::

    $ ./bin/buildout bootstrap

Run buildout::

    $ ./bin/buildout

Start Plone in foreground::

    $ ./bin/instance fg


Running tests
-------------

    $ tox

list all tox environments::

    $ tox -l
    plone52-py38
    plone60-py311

run a specific tox env::

    $ tox -e plone60-py311
