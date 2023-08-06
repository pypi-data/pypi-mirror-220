=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

`0.0.2`_ (2023-07-22)

Changed
~~~~~~~

* Atoms type replaced with typing.Self in ``atoms.pyi``
* Increased specification of container data types where possible
* Replacement of ``numpy.ndarray`` with generic ``numpy.typing.NDArray``
* Increased use of abstract base classes (e.g., ``numbers.Real``, ``colllections.abc.Iterable``, ``numpy.integer``, etc.)

`0.0.1`_ (2023-07-22)

Added
~~~~~

* ``atoms.pyi`` stub file.

Removed
~~~~~~~

* ``atom.pyi`` and ``cell.pyi`` stub files

`0.0.0`_ (2023-07-21)
---------------------

Added
~~~~~

* First release on PyPI.

.. _`0.0.0`: https://gitlab.com/ugognw/ase-stubs/-/tree/v0.0.0?ref_type=tags
.. _`0.0.1`: https://gitlab.com/ugognw/ase-stubs/-/tree/v0.0.1?ref_type=tags
