
.. currentmodule:: perennial

.. _reference:

Perennial reference
===================

Journal
-------

Perennial journals can record text and mood entries with :py:func:`Journal.record`. Journal entries may also be associated with a file — such as a Markdown file representing a more comprehensive journal entry, or even a directory of another perennial journal. Streaks are automatically tallied. The default mode to track streak is weekly.

.. autoclass:: Journal
   :members:

Entry
-----

Use :py:func:`Journal.record` to record new entries, and search or iterate through a journal (``for entry in journal: ...``) to retrieve previous entries.

.. autoclass:: Entry
   :members:

Goal
----

Use :py:func:`Journal.goal` to set or get the states of goals. :py:func:`Journal.time_in_state` returns the amount of time a goal has been in a state (optionally given a time range). Use :py:func:`Journal.goals` to iterate through the current states of goals. And use :py:func:`Journal.goals_in_state` to lookup which goals are in a given state.

.. autoclass:: Goal
   :members:

StreakCheck
-----------

.. autoclass:: StreakCheck

   Different ways to keep track of a journaling streak. While a daily streak can keep an individual pressured to maintain consistency every day, missing only a single day then feels demotivating. Changing the perspective to a weekly, monthly, or yearly streak can help bring back motivation by allowing flexibility, leniency, and time to slow down.

   .. autoattribute:: StreakCheck.DAILY

      Represents keeping a daily streak, like Duolingo.

   .. autoattribute:: StreakCheck.WEEKLY

      Represents keeping a journal streak, week-to-week, like weekly check-ins or self-care nights.

   .. autoattribute:: StreakCheck.MONTHLY

      Represents keeping a journal streak by month, like tracking menstrual cycles.

   .. autoattribute:: StreakCheck.YEARLY

      Represents keeping a streak on a yearly basis, like New Year's resolutions.

Exceptions
----------

.. autoclass:: PerennialException

.. autoclass:: ZeroEntriesFound

