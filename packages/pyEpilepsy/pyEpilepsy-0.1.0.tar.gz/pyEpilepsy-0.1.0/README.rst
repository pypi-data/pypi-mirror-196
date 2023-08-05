=============
pyEpilepsy
=============

|Tests|_ |Doc|_ |Codecov|_

.. |Tests| image:: https://github.com/etiennedemontalivet/pyepilepsy/actions/workflows/main.yml/badge.svg
.. _Tests: https://github.com/etiennedemontalivet/pyEpilepsy/actions/workflows/main.yml

.. |Doc| image:: https://github.com/etiennedemontalivet/pyepilepsy/actions/workflows/documentation.yml/badge.svg
.. _Doc: https://github.com/etiennedemontalivet/pyEpilepsy/actions/workflows/documentation.yml


.. |Codecov| image:: https://codecov.io/gh/etiennedemontalivet/pyEpilepsy/branch/master/graph/badge.svg?token=MH99PGHU1C
.. _Codecov: https://codecov.io/gh/etiennedemontalivet/pyEpilepsy?branch=master


This repository provides code for epilepsy seizure forecasting.
The documentation of the pyEpilepsy module is available at: 
`documentation <https://etiennedemontalivet.github.io/pyepilepsy/index.html>`_.

Installation
------------

To install the package, the simplest way is to use pip to get the latest release::

  $ pip install pyepilepsy


Work to be done
---------------

This repo only covers metrics for seizure forecasting for now. I plan to add some other features such as:

* common databases data parsing to mne format
    * chb-mit
    * ...
* data labellisation
    * for binary classification (*preictal* vs *interictal*)
    * for regression (time before seizure)
* ...

Contribution
------------

Any contribution is welcomed. If you want to collaborate on this repo, feel free to reach me by private message.