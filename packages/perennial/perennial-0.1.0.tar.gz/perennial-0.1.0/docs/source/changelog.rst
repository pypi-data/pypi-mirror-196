
.. currentmodule:: perennial

.. _changelog:

Version history
===============

Version related info
--------------------

There are two main ways to query version information about the library.

.. data:: version_info

   A named tuple of the form ``major.minor.build``, where:

   - ``major`` is a major release, representing either many new features or a significant refactor to the underlying API or API wrapper.

   - ``minor`` is a minor release, representing some new features on the given major release.

   - ``build`` is incremented for each latest build, patch, or revision of a minor release.

.. data:: __version__

   A string representation of the version. e.g. ``"0.1.23"``.

.. Most common headings would be New features, Fixes, Improvements

.. _whats_new:

2023-03-10F: v0.1.0
-------------------

Ready for `PyPI <https://pypi.org/project/perennial/>`_!

2023-02-04S: v0.0.3
-------------------

The Fundamentals
~~~~~~~~~~~~~~~~

- `~perennial.Journal`
- `~perennial.Entry`
- `~perennial.Goal`
- `~perennial.StreakCheck`
