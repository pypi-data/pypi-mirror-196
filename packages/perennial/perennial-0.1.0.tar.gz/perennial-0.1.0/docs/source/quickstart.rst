
.. currentmodule:: perennial

.. _getting_started:

Getting started
===============

Prerequisites
-------------

Perennial is intended to work with Python 3.9 or higher.

Installing
----------

Use pip like usual: ::

   pip install -U perennial

.. _`virtual environments`: https://docs.python.org/3/tutorial/venv.html

Development
-----------

If you'd like to explore the repo or experiment with your own changes and potentially contribute to development: ::

   git clone https://almonds.dev/git/perennial
   cd perennial
   pip install -e ."[dev]"

Basic concepts
--------------

This section describes how to use the command-line options for creating journals, adding entries, and tracking goals. See the :ref:`reference` for information on how to interface with your journals more directly.

Run ``python -m perennial -h`` for help.

``init``
~~~~~~~~

Initialize a journal in the current working directory: ::

   python -m perennial init 'Journal full of examples'

Specify a journal elsewhere with the ``-d`` (``--database``) flag: ::

   python -m perennial -d ~/journals/test/ init 'Journal full of examples'

This flag is settable for all subcommands. The default is the current working directory.

Each journal entry can optionally be associated with a file. The ``init`` command can take a template file with the ``-t`` (``--template``) flag: ::

   python -m perennial init 'Journal full of examples' -t ~/journals/test/template.md

When recording a new entry with an associated file, this template file will be copied over if the file does not already exist.

The journal's streak-tracking mode can be set with the ``-s`` (``--streak-mode``) flag: ::

   python -m perennial init 'Journal full of examples' -s daily

Currently, the supported streak-tracking modes are: ``daily``, ``weekly``, ``monthly``, and ``yearly``. The default journal streak-tracking mode is ``weekly``.

``record``
~~~~~~~~~~

Record an entry with: ::

   python -m perennial record 'This is an example entry.'

Specify a mood for the entry with ``-m`` (``--mood``). Mood values are integers.

Associate a file with the new entry using ``-f`` (``--file``): ::

   python -m perennial record 'This is an example entry.' -f example-entry.md

``goal``
~~~~~~~~

Update the status of a goal with the ``goal`` subcommand by specifying the name of the goal followed by the goal state: ::

   python -m perennial goal 'Example goal' DONE

Use whichever goal-tracking system you like. I prefer sticking with these goal states: ``TODO``, ``DOING``, ``DONE``, ``CANCELED``.

``check``
~~~~~~~~~

Finally, check up on your journals with the ``check`` command: ::

   python -m perennial check

