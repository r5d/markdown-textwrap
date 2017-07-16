-*- mode: rst; coding: utf-8;  -*-

HACKING
=======

Setting up the environment
--------------------------

First setup virtual environment::

   cd markdown-link-style
   virtualenv --python=python3.5 .

Activate virtual environment::

   source bin/activate

Install dependencies::

   pip install -r requirements.txt
   python setup develop

Running tests
-------------

Run all tests::

   nosetests -sv


Run a particular test class::

   nosetests -sv tests.module_name:TestClassName

Run a particular test in a test class::

   nosetests -sv tests.module_name:TestClasseName.test_method_name
