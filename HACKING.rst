-*- mode: rst; coding: utf-8;  -*-

HACKING
=======

Setting up the environment
--------------------------

First setup virtual environment::

   ./venv.sh

Activate virtual environment::

   source venv/bin/activate

Setup development environment::

  ./bootstrap.sh

Running tests
-------------

Run all tests::

   nosetests -sv


Run a particular test class::

   nosetests -sv tests.module_name:TestClassName

Run a particular test in a test class::

   nosetests -sv tests.module_name:TestClasseName.test_method_name
