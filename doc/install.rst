===============================
Installing `spyre`
===============================

.. _install_from_github:

Installing from GitHub
======================

At the moment, the only way to get ``spyre`` is from `GitHub <https://github.com/bl0b/spyre>`_.

I also recommend to use `virtualenv <http://pypi.python.org/pypi/virtualenv>`_ and `pip <http://pypi.python.org/pypi/pip>`_ to work with this repository.

To get the sources and install all the requirements::

    git clone git://github.com/bl0b/spyre.git
    cd spyre
    virtualenv env
    source virtualenv/bin/activate
    pip install -r requirements.txt
    pip install -r requirements-test.txt

.. _testing:

Testing
=======

First you need to install all the requirements for the tests, following the previous instruction. Then, you can easily run the tests with the following command::

    ./run_tests.py
