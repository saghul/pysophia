========
pysophia
========

Overview
========

pysophia is a Python (CFFI based) library wrapping the `Sophia library <http://sphia.org>`_.

    Sophia is a modern embeddable key-value database designed for a high load environment.

    It has unique architecture that was created as a result of research and rethinking of primary algorithmical
    constraints, associated with a getting popular Log-file based data structures, such as LSM-tree.


NOTE: pysophia is still in early development, not all features all implemented yet, see below.


Not (yet) implemented features
==============================

* Cursors
* Transactions
* Maybe some of the options from sp_ctl


API
===

The entire API is contained in a single class, unsurprisingly, ``Sophia``.

Creating (or opening an existing) database::

    db = Sophia('myDB', flags=Sophia.FL_CREAT|Sofia.FL_RDWR)

Setting a value for a given key::

    db.set('foo', 'bar')

Getting the value assigned to a key::

    db.get('foo')

Deleting a key::

    db.delete('foo')

Closing the database, all further operations will raise an exception::

    db.close()


Author
======

Saúl Ibarra Corretgé <saghul@gmail.com>


License
=======

Unless stated otherwise on-file pysophia uses the MIT license, check LICENSE and NOTICE files.


Contributing
============

If you'd like to contribute, fork the project, make a patch and send a pull
request. Have a look at the surrounding code and please, make yours look
alike :-) If you intend to contribute a new feature please contact the maintainer
beforehand in order to discuss the design.

