===============================
PyMaybe
===============================

.. image:: https://travis-ci.org/ekampf/pymaybe.svg?branch=master
        :target: https://travis-ci.org/ekampf/pymaybe
        
.. image:: https://img.shields.io/pypi/v/pymaybe.svg
        :target: https://pypi.python.org/pypi/pymaybe

A Python implementation of the Maybe pattern.

Installation
------------

    pip install pymaybe
    
Getting Started
---------------

    from pymaybe import maybe
    first_name = maybe(deep_hash)['account']['user_profile']['first_name'].or_else("<unknown>")

Documentation
-------------
Maybe monad is a programming pattern that allows to treat None values that same way as non-none values. 
This is done by wrapping the value, which may or may not be None to, a wrapper class.

The implementation includes two classes: *Maybe* and *Something*.
*Something* represents a value while *Nothing* represents a None value.
There's also a method *maybe* which wraps a regular value and and returns *Something* or *Nothing* instance.

::

    >>> maybe("I'm a value")
    "I'm a value"
    
    >>> maybe(None);
    None
    
Both *Something* and *Nothing* implement 4 methods allowing you to test their real value: *is_some*, *is_none*, *get* and *or_else*

::

    >>> maybe("I'm a value").is_some()
    True
    
    >>> maybe("I'm a value").is_none()
    False
    
    >>> maybe(None).is_some()
    False
    
    >>> maybe(None).is_none()
    True
    
    >>> maybe("I'm a value").get()
    "I'm a value"
    
    >>> maybe("I'm a value").or_else(lambda: "No value")
    "I'm a value"
    
    >>> maybe(None).get()
    Traceback (most recent call last):
    ...
    Exception: No such element

    >>> maybe(None).or_else(lambda: "value")
    'value'

    >>> maybe(None).or_else("value")
    'value'

In addition, *Something* and *Nothing* implement the Python magic methods allowing you to treat them as dictionaries:

::

    >>> nested_dict['store']['name']
    'MyStore'

    >>> nested_dict['store']['address']
    None

    >>> nested_dict['store']['address']['street'].or_else('No Address Specified')
    'No Address Specified'

All other method calls on *Something* are forwarded to its real *value*:

::

    >>> maybe('VALUE').lower()
    'value'
    
    >>> maybe(None).invalid().method().or_else('unknwon')
    'unknwon'
    
Examples & Use Cases
--------------------

Parsing deep JSON objects where some items might be missing.
Without maybe:

::

    stores = json.get('stores')
    if stores:
        products = stores[0].get('products')
        if products:
            product_name = products[0].get('details', {}).get('name') or 'unknown'

With maybe:

::
    
    product_name = maybe(stores)[0]['products'][0]['details']['name'].or_else('unknown')


Getting the current logged in user's name.
Without maybe:

::

    def get_user_name():
        current_user = request.user
        if current_user:
            return current_user.name
        
        return ''
        
With maybe:

::

    def get_user_name():
        return maybe(request.user).name.or_else('')

Further Reading
---------------

* `Option (Scala) <http://www.scala-lang.org/api/current/scala/Option.html>`_
* `Maybe (Java) <https://github.com/npryce/maybe-java>`_
* `Maybe pattern (Python recipe) <http://code.activestate.com/recipes/577248-maybe-pattern/>`_
* `Data.Maybe (Haskell) <http://www.haskell.org/ghc/docs/latest/html/libraries/base/Data-Maybe.html>`_
* `Maybe (Ruby) <https://github.com/bhb/maybe>`_

Copyright and License
---------------------
Copyright 2015 - Eran Kampf

* Free software: BSD license
* Documentation: https://pymaybe.readthedocs.org.
