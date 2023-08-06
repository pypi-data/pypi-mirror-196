#!/usr/bin/env python3

import sqlite3
from pathlib import Path
import shutil
from dataclasses import dataclass
from typing import Callable, Generator, Optional
from datetime import datetime, date, timedelta
from enum import Enum

class PerennialException(Exception):
   """Base class for all perennial exceptions
   """

class ZeroEntriesFound(PerennialException):
   """Raised when no entries were found in the entries or goals table
   """

_date_formats = (
   "%Y-%m-%d",
   "%Y-%m-%d %H:%M:%S.%f",
   "%Y-%m-%dT%H:%M:%S.%f",
   "%Y-%m-%d %H:%M",
   "%Y-%m-%d %H:%M:%S",
   "%Y-%m-%dT%H:%M:%S",
   "%Y-%m-%d %I:%M%p",
   "%Y-%m-%d %I:%M:%S %p",
   "%m/%d/%Y"
)

def _parse_date(when: Optional[datetime | str]) -> datetime:
   """Converts str to datetime, if not already datetime
   """
   if when is None: when = datetime.today()
   if isinstance(when, str):
      for fmt in _date_formats:
         try:
            when = datetime.strptime(when, fmt)
            break
         except ValueError:
            pass
   if isinstance(when, str):
      raise ValueError(f"could not parse datetime from {when!r}")
   return when

def _next_week_number(last: date) -> int:
   week = last.isocalendar()[1]
   while True:
      last += timedelta(days=1)
      next_week = last.isocalendar()[1]
      if week != next_week:
         return next_week

def _format_date(when: Optional[datetime]=None) -> str:
   """Returns a string representing today's date

   For example, Saturday February 4, 2023 would be "2023-02-04S"
   """
   when = datetime.today() if when is None else when
   weekday = "NMTWRFS"[int(when.strftime("%w"))]
   return when.strftime("%Y-%m-%d") + weekday

"""
These functions bump the provided streak if two datetimes are considered
adjacent. They also assert that the order of the datetimes provided is
*ascending*.

>>> last = datetime(2022, 12, 31)
>>> next = datetime(2023, 1, 1)
>>> streak = 99
>>> 
>>> _yearly(last, next, streak) # adjacent years
100
>>> _monthly(last, next, streak) # adjacent months
100
>>> _weekly(last, next, streak) # same week number
99
>>> _daily(last, next, streak) # adjacent days
100
>>>
"""

def _yearly(last: datetime, next: datetime, streak: int) -> int:
   """Check if two datetimes form a yearly streak
   """
   assert next >= last

   if last.year + 1 == next.year:
      return streak + 1
   elif last.year == next.year:
      return streak
   
   return 1

def _monthly(last: datetime, next: datetime, streak: int) -> int:
   """Check if two datetimes form a monthly streak
   """
   assert next >= last

   forms_streak = (last.year, last.month + 1) == (next.year, next.month)
   forms_streak = forms_streak or \
      (last.year + 1, last.month, next.month) == (next.year, 12, 1)

   if forms_streak:
      return streak + 1
   elif (last.year, last.month) == (next.year, next.month):
      return streak

   return 1

def _weekly(last: datetime, next: datetime, streak: int) -> int:
   """Check if two datetimes form a weekly streak
   """
   assert next >= last

   if next - last >= timedelta(weeks=2): return 1
   last_week = last.date().isocalendar()[1]
   next_week = next.date().isocalendar()[1]

   if next_week == _next_week_number(last.date()):
      return streak + 1
   elif last_week == next_week:
      return streak
   
   return 1

def _daily(last: datetime, next: datetime, streak: int) -> int:
   """Check if two datetimes form a daily streak
   """
   assert next >= last

   last_day = last.date()
   next_day = next.date()

   if next_day - last_day == timedelta(days=1):
      return streak + 1
   elif next_day == last_day:
      return streak

   return 1

class StreakCheck(Enum):
   YEARLY = "yearly"
   MONTHLY = "monthly"
   WEEKLY = "weekly"
   DAILY = "daily"

_checkers: dict[StreakCheck, Callable[[datetime, datetime, int], int]] = {
   StreakCheck.YEARLY: _yearly,
   StreakCheck.MONTHLY: _monthly,
   StreakCheck.WEEKLY: _weekly,
   StreakCheck.DAILY: _daily,
}

@dataclass(frozen=True, order=True)
class Entry:
   """Represents a journal entry

   Attributes:
      when: Date of journal entry
      content: Journal entry summary
      file: Associated file, if any, as a relative path
      mood: Mood level
      streak: Daily streak
   """
   when: datetime
   content: str
   file: Optional[Path]
   mood: Optional[int]
   streak: int

@dataclass(frozen=True, order=True)
class Goal:
   """Represents a goal and its state

   Attributes:
      when: Date of goal state entry
      name: Exact name of goal
      state: State of goal
   """
   when: datetime
   name: str
   state: str

class Journal:
   """Represents a journal

   Args:
      content: Name or description of this journal

   Keyword args:
      file: Path to the journal's SQLite database or the path to the journal's directory that
         contains the SQLite database. The database is initialized if it does not already exist.
      streak_mode: The function that computes the streak number given two datetimes and a
         running streak.

   Attributes:
      when: When this journal was created
      content: Name or description of this journal
      file: Path to the SQLite database
      streak_mode: The streak mode, as saved in the database
      template: Path to a template file to use for new journal entries
      directory: Path containing the journal (readonly)
      db: SQLite database connection (readonly)

   Tip:
      Iterate through the journal entries with ``for entry in journal``
   """
   def __init__(self, content: Optional[str]=None, *,
      file: Optional[Path | str]=None,
      streak_mode: StreakCheck=StreakCheck.WEEKLY,
      template: Optional[Path | str]=None,
   ):
      content = content if content is not None else _format_date()

      self.file = Path(file) if file is not None else Path.cwd()
      # allow directories
      if self.file.exists() and self.file.is_dir():
         self.file /= "journal.db"

      if template:
         template_path = Path(template)
         if not template_path.exists():
            raise FileNotFoundError(f"template `{template}` doesn't seem to exist")
         if template_path.is_absolute():
            self.template = template_path.relative_to(self.directory)
         else:
            self.template = template_path
         self.template = self.template
      else:
         self.template = None

      # set up connection
      self._database_connection = sqlite3.connect(self.file)
      cursor = self.db.cursor()

      # Meta table
      cursor.execute("""
         CREATE TABLE IF NOT EXISTS meta (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            content TEXT NOT NULL,
            streak_mode TEXT NOT NULL,
            template TEXT NULL
         );
      """)

      cursor.execute("""
         CREATE TRIGGER IF NOT EXISTS prevent_multiple_rows
         BEFORE INSERT ON meta
         BEGIN
            SELECT RAISE(FAIL, "Only one row defines the meta table")
            WHERE (SELECT COUNT(*) FROM meta) > 0;
         END;
      """)

      try:
         cursor.execute("""
            INSERT INTO meta (date, content, streak_mode, template) VALUES (?, ?, ?, ?);
         """, (datetime.now(), content, streak_mode.value, self.template))
      except sqlite3.IntegrityError:
         pass

      # Journal entries table
      cursor.execute("""
         CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            content TEXT NOT NULL,
            streak INTEGER NOT NULL,
            mood INTEGER NULL,
            file TEXT NULL
         );
      """)

      # Goal updates table
      cursor.execute("""
         CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            name TEXT NOT NULL,
            state TEXT NOT NULL
         );
      """)

      self.db.commit()
      self.update()

   def update(self, **kwargs):
      expected = ("when", "content", "streak_mode", "template")
      unexpected = ", ".join([repr(k) for k in kwargs if k not in expected])
      assert not unexpected, \
         f"found unexpected kwargs in `Journal.update()`: {unexpected}"

      cursor = self.db.cursor()
      cursor.execute("""
         SELECT id, date, content, streak_mode, template
         FROM meta
         ORDER BY date DESC
         LIMIT 1;
      """)
      id, when, content, streak_mode, template = cursor.fetchone()
      self.when = _parse_date(when)
      self.content = content
      self.streak_mode = StreakCheck(streak_mode)
      self.template = None if template is None else Path(template)

      if kwargs:
         template_path = kwargs.get("template", self.template)
         if template_path is not None:
            template_path = Path(template_path).relative_to(self.directory).as_posix()
         new_info = (
            _parse_date(kwargs.get("when", self.when)),
            str(kwargs.get("content", self.content)),
            StreakCheck(kwargs.get("streak_mode", self.streak_mode)).value,
            template_path,
         )
         cursor.execute("""
            UPDATE meta
            SET date = ?,
                content = ?,
                streak_mode = ?,
                template = ?
            WHERE id = ?;
         """, new_info + (id,))

         self.db.commit()

   @property
   def directory(self):
      return self.file.parent

   @property
   def db(self):
      return self._database_connection

   #
   # Journal stuff
   #

   def record(self, content: Optional[str]=None, *,
      mood: Optional[int]=None,
      when: Optional[datetime | str]=None,
      file: Optional[Path]=None
   ) -> Entry:
      """Record a journal entry

      Returns:
         Entry
      """
      when = _parse_date(when)

      content = content if content else _format_date()

      # Handle entry file (may be a directory, that's fine)
      if file:
         file = Path(file)
         if not file.exists():
            if self.template and self.template.exists():
               shutil.copy2(self.template, file)
            else:
               file.touch()
         if file.is_absolute():
            relative_file_path = file.relative_to(self.directory)
         else:
            relative_file_path = file
         relative_file_path = relative_file_path.as_posix()
      else:
         relative_file_path = None

      # Handle streak by checking the latest journal entry before this one
      cursor = self.db.cursor()
      cursor.execute("""
         SELECT date, streak
         FROM entries
         WHERE date <= ?
         ORDER BY date DESC
         LIMIT 1;
      """, (when,))
      last_entry = cursor.fetchone()
      if last_entry is None:
         next_streak = 1
      else:
         last_date, last_streak = last_entry
         last_date = _parse_date(last_date)
         next_streak = _checkers[self.streak_mode](last_date, when, last_streak)

      # Add the new entry
      cursor.execute("""
         INSERT INTO entries (date, content, streak, mood, file)
         VALUES (?, ?, ?, ?, ?);
      """, (when, content, next_streak, mood, relative_file_path))
      self.db.commit()

      return Entry(when, content, file, mood, next_streak)

   def __iter__(self) -> Generator[Entry, None, None]:
      cursor = self.db.cursor()
      cursor.execute("""
         SELECT date, content, file, mood, streak
         FROM entries
         ORDER BY date ASC;
      """)
      for when, content, file, mood, streak in cursor:
         when = _parse_date(when)
         yield(Entry(when, content, file, mood, streak))

   def __len__(self) -> int:
      count = 0
      for _ in self.__iter__(): count += 1
      return count

   def search(self, search_term=None, *,
      start_date: Optional[datetime | str]=None,
      end_date: Optional[datetime | str]=None
   ) -> list[Entry]:
      """Retrieve journal entries (optionally containing a specified search term)

      Args:
         search_term (Optional): Search term to look for. If not provided, returns all entries.
         start_date (Optional): Earliest date to search. If not provided, uses date of earliest journal entry.
         end_date (Optional): Latest date to search. If not provided, uses today's date.

      Note:
         Iterate through the journal directly if you want all entries.
      """
      if search_term is None:
         return list(self)

      if start_date is None:
         entry = None
         for entry in self: break
         if entry is None: return []
         start_date = entry.when
      start_date = _parse_date(start_date)
      end_date = _parse_date(end_date)

      cursor = self.db.cursor()
      cursor.execute("""
         SELECT date, content, file, mood, streak
         FROM entries
         WHERE content LIKE ? AND date >= ? AND date <= ?
         ORDER BY date DESC;
      """, (f"%{search_term}%", start_date, end_date))

      results = []
      for when, content, file, mood, streak in cursor:
         when = _parse_date(when)
         results.append(Entry(when, content, file, mood, streak))

      return results

   def streak(self, when: Optional[datetime | str]=None) -> int:
      """Get streak for given date

      Args:
         when (Optional): Date to look up streak. If not provided, uses today's date.
      """
      when = _parse_date(when)

      # Latest journal entry at the given date
      cursor = self.db.cursor()
      cursor.execute("""
         SELECT streak
         FROM entries
         WHERE date <= ?
         ORDER BY date DESC
         LIMIT 1;
      """, (when,))
      entry = cursor.fetchone()
      if entry is None: return 0 #raise ZeroEntriesFound
      streak, = entry
      return streak

   def random(self) -> Entry:
      """Retrieve a single random journal entry

      Todo: add start_date and end_date kwargs

      Raises:
         ZeroEntriesFound: when there are no journal entries yet
      """
      cursor = self.db.cursor()
      cursor.execute("""
         SELECT date, content, file, mood, streak
         FROM entries
         ORDER BY RANDOM()
         LIMIT 1;
      """)
      entry = cursor.fetchone()
      if entry is None: raise ZeroEntriesFound
      when, content, file, mood, streak = entry
      when = _parse_date(when)
      return Entry(when, content, file, mood, streak)

   def sync(self):
      """Synchronize the streak column of the journal entries
      """
      cursor = self.db.cursor()

      # Get all the journal entries sorted by date
      cursor.execute("""
         SELECT id, date
         FROM entries
         ORDER BY date ASC;
      """)
      entries = cursor.fetchall()

      # Iterate through the journal entries from oldest to newest
      last_entry_date = None
      streak = 1
      for id, when in entries:
         entry_date = datetime.fromisoformat(when)

         # Restart or continue the streak based on the difference between the
         # current and previous entry dates
         if last_entry_date is None:
            pass
         else:
            streak = _checkers[self.streak_mode](last_entry_date, entry_date, streak)

         # Update the streak in the database
         cursor.execute("""
            UPDATE entries
            SET streak = ?
            WHERE id = ?;
         """, (streak, id))

         last_entry_date = entry_date

      # Save the changes to the database
      self.db.commit()

   #
   # Goal stuff
   #

   def goals(self, all=False) -> Generator[Goal, None, None]:
      """Iterate through goals

      Args:
         all: Default False, iterate only through the most recent goal states.
            If True, iterate through all goals items recorded in this journal.
      """
      cursor = self.db.cursor()
      if all:
         cursor.execute("""
            SELECT date, name, state
            FROM goals
            ORDER BY date ASC;
         """)
      else:
         cursor.execute("""
            SELECT date, name, state
            FROM goals
            ORDER BY date DESC;
         """)
      seen = set()
      for entry in cursor:
         when, name, state = entry
         if not all and name in seen: continue
         when = _parse_date(when)
         seen.add(name)
         yield Goal(when, name, state)

   def goal(self, name: str, state: Optional[str]=None, *,
      when: Optional[datetime | str]=None,
   ) -> Goal:
      """Get or set goal state

      Args:
         name: Name of goal (must be exact)
         state (Optional): State to assign to goal. If not provided, the current goal state is returned instead.
         when (Optional): The date to set or get the goal state. If not provided, uses today's date.

      Raises:
         ZeroEntriesFound: if the goal provided was not found in the goals table

      Returns:
         Optional[str]
      """
      when = _parse_date(when)

      cursor = self.db.cursor()

      # Get goal state
      if state is None:
         cursor.execute("""
            SELECT date, name, state
            FROM goals
            WHERE date <= ? AND name = ?
            ORDER BY date DESC
            LIMIT 1;
         """, (when, name))
         goal = cursor.fetchone()
         if goal is None: raise ZeroEntriesFound
         when, name, state_ = goal
         when = _parse_date(when)
         return Goal(when, name, state_)

      # Or set goal state
      cursor.execute("""
         INSERT INTO goals (date, name, state)
         VALUES (?, ?, ?);
      """, (when, name, state))
      self.db.commit()

      return Goal(when, name, state)

   def goals_in_state(self, state: str, *,
      start_date: Optional[datetime | str]=None,
      end_date: Optional[datetime | str]=None
   ) -> set[Goal]:
      """Return set of all goals *currently* in the given state

      Args:
         state: State of goals to look for
         start_date (Optional): Earliest date to look through journal. If not provided, uses date of earliest journal entry.
         end_date (Optional): Latest date to look through journal. If not provided, uses today's date.
      """
      if start_date is None:
         goal = None
         for goal in self.goals(all=True): break
         if goal is None: return set()
         start_date = goal.when
      start_date = _parse_date(start_date)
      end_date = _parse_date(end_date)

      seen = set()
      goals = set()

      # Look up all entries within the time range
      cursor = self.db.cursor()
      cursor.execute("""
         SELECT date, name, state
         FROM goals
         WHERE date >= ? AND date <= ?
         ORDER BY date DESC;
      """, (start_date, end_date))
      entries = cursor.fetchall()

      # Only count the ones that are *currently* in the given state
      for when, name, state_ in entries:
         if name not in seen:
            seen.add(name)
            if state_ == state:
               goals.add(Goal(when, name, state))

      return goals

   def time_in_state(self, name: str, state: str, *,
      start_date: Optional[datetime | str]=None,
      end_date: Optional[datetime | str]=None
   ) -> timedelta:
      """Tallies up the total time a goal has been in a given state

      Args:
         name: Name of goal (must be exact)
         state: State of goal

      Keyword args:
         start_date: Earliest date to look through journal.
            If not provided, uses date of earliest journal entry.
         end_date: Latest date to look through journal. If not provided, uses today's date.
      
      Returns:
         timedelta
      """
      if start_date is None:
         goal = None
         for goal in self.goals(all=True): break
         if goal is None: return timedelta(0)
         start_date = goal.when
      start_date = _parse_date(start_date)
      end_date = _parse_date(end_date)

      # Look up all entries with the specified goal name, state, and time range
      cursor = self.db.cursor()
      cursor.execute("""
         SELECT date, state
         FROM goals
         WHERE name = ? AND date >= ? AND date <= ?
         ORDER BY date ASC;
      """, (name, start_date, end_date))
      entries = cursor.fetchall()

      # Calculate the total time spent in the state
      total_time = timedelta(0)
      if not entries: return total_time

      for last_entry, next_entry in zip(entries, entries[1:]):
         last_date, last_state = last_entry
         next_date, _          = next_entry
         last_date = _parse_date(last_date)
         next_date = _parse_date(next_date)
         if last_state == state:
            # add the time between this entry and the next one
            if next_date < end_date:
               total_time += next_date - last_date
            else:
               total_time += end_date - last_date
               return total_time

      # Add the time between the last entry and the end date
      final_date, final_state = entries[-1]
      final_date = _parse_date(final_date)
      if final_date < end_date and final_state == state:
         total_time += end_date - final_date

      return total_time

