Installation
-------------

.. code:: bash

    pip install sponge-test

Usage
---------

Command Line
==============

.. code:: bash

    sponge-test [options]

For example::

    sponge-test -s -v -k rmsd

Python Script
==============

There are 6 built-in systems

1. water
2. H2O2
3. dipeptide
4. ala12
5. bad_water
6. bad_dipeptide

For each system, there are two attributes named "prefix" and "description".

.. code:: python

    from sponge_test import water
    import os
    print(water.prifix, water.description)
    assert os.system(f"SPONGE -default_in_file_prefix {water.prefix}") == 0
