from datetime import datetime, timedelta
import unittest
import time
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.append("..")
from perennial import (
   Journal, StreakCheck, ZeroEntriesFound,
   Goal, Entry,
)

class TestCreation(unittest.TestCase):
   """
   Make sure that journal creation works and leaves a journal.db file that may
   be accessed later.
   """
   def setUp(self):
      """Perform setup before each test
      """
      self.temp_dir = Path(tempfile.mkdtemp()).resolve()
   
   def tearDown(self):
      """perform cleanup after each test
      """
      Path("journal.db").unlink(missing_ok=True)
      Path("tests/journal.db").unlink(missing_ok=True)
      shutil.rmtree(self.temp_dir, ignore_errors=True)

   def test_persistence_cwd(self):
      """
      Make sure journals can be created and persist in the current working
      directory (namely, when the `file` arg isn't provided)
      """
      j = Journal("Test journal", streak_mode=StreakCheck.DAILY)
      del j
      time.sleep(0.1)

      j = Journal()
      self.assertEqual(j.content, "Test journal")
      self.assertEqual(j.streak_mode, StreakCheck.DAILY)

   def test_persistence_relative_directory(self):
      """
      Make sure journals can be created and persist given a relative path
      """
      j = Journal("Test journal", streak_mode=StreakCheck.DAILY, file="./tests/")
      del j
      time.sleep(0.1)

      j = Journal(file="./tests/")
      self.assertEqual(j.content, "Test journal")
      self.assertEqual(j.streak_mode, StreakCheck.DAILY)

   def test_persistence_absolute_directory(self):
      """
      Make sure journals can be created and persist given an absolute path
      """
      j = Journal("Test journal", streak_mode=StreakCheck.DAILY, file=self.temp_dir)
      del j
      time.sleep(0.1)

      j = Journal(file=self.temp_dir)
      self.assertEqual(j.content, "Test journal")
      self.assertEqual(j.streak_mode, StreakCheck.DAILY)

class TestTrackMood(unittest.TestCase):
   """
   Add some entries with moods, then confirm that it persists.
   """
   def tearDown(self):
      """perform cleanup after each test
      """
      Path("journal.db").unlink(missing_ok=True)

   def test_moods_persistence(self):
      """Make sure journal *entries* persist
      """
      j = Journal("Test journal")

      today = datetime.now()
      moods = [1, None, 2, 3, 4, None, 5]
      whens = [today - timedelta(days=t) for t in range(len(moods), 0, -1)]
      for w, m in zip(whens, moods):
         j.record("Test entry", mood=m, when=w)
      del j
      time.sleep(0.1)

      j = Journal()
      for e in j:
         self.assertIsInstance(e, Entry)
         self.assertIsInstance(e.when, datetime)

      self.assertEqual(len(j), len(moods))

      persisted_moods = [e.mood for e in j]
      self.assertEqual(persisted_moods, moods)

class TestTrackStreak(unittest.TestCase):
   """
   Make sure all the streak tracker functions work. Probably the most technical
   puzzle here to test.
   """
   def tearDown(self): Path("journal.db").unlink(missing_ok=True)

   def test_daily_streak_checker(self):
      """
      Make sure DAILY streak tracking works
      """
      j = Journal("Test journal", streak_mode=StreakCheck.DAILY)

      data = {
         datetime(2022,  1, 21): 1,
         datetime(2022,  1, 22): 2,
         datetime(2022,  1, 23): 3,
         datetime(2022,  1, 24): 4,
         datetime(2022,  1, 24): 4,
         datetime(2022,  1, 24): 4,
         datetime(2022,  1, 24): 4,
         datetime(2022,  1, 25): 5,
         datetime(2022,  1, 26): 6,
         datetime(2022,  1, 27): 7,
         datetime(2022,  1, 28): 8,
         datetime(2022,  1, 29): 9,
         datetime(2022,  1, 30): 10,
         datetime(2022,  1, 31): 11,
         datetime(2022,  2,  1): 12,
         datetime(2022,  2,  2): 13,
         datetime(2022,  2,  3): 14,
         datetime(2022,  2,  7): 1,
         datetime(2022,  2,  8): 2,
         datetime(2022,  2,  8): 2,
         datetime(2022,  2, 10): 1,
         datetime(2022,  2, 12): 1,
      }
      for when in data: j.record("Test entry", when=when)
      del j
      time.sleep

      j = Journal()
      persisted_streaks = [e.streak for e in j]

      self.assertListEqual(persisted_streaks, list(data.values()))

   def test_weekly_streak_checker(self):
      """
      Make sure DAILY streak tracking works

      Remember that the first day of each week is on a Monday
      """
      j = Journal("Test journal", streak_mode=StreakCheck.WEEKLY)

      data = {
         datetime(2022, 12,  5): 1,
         datetime(2022, 12, 12): 2,
         datetime(2022, 12, 19): 3,
         datetime(2022, 12, 25): 3,
         datetime(2022, 12, 26): 4,
         datetime(2022, 12, 31): 4,
         datetime(2023,  1,  1): 4,
         datetime(2023,  1,  2): 5,
         datetime(2023,  1,  9): 6,
         datetime(2023,  1, 23): 1,
         datetime(2023,  2,  3): 2,
      }
      for when in data: j.record("Test entry", when=when)
      del j
      time.sleep

      j = Journal()
      persisted_streaks = [e.streak for e in j]

      self.assertListEqual(persisted_streaks, list(data.values()))

   def test_monthly_streak_checker(self):
      """
      Make sure MONTHLY streak tracking works
      """
      j = Journal("Test journal", streak_mode=StreakCheck.MONTHLY)

      data = {
         datetime(2022,  1,  1): 1,
         datetime(2022,  1,  2): 1,
         datetime(2022,  1, 23): 1,
         datetime(2022,  2,  1): 2,
         datetime(2022,  3,  5): 3,
         datetime(2022,  4, 12): 4,
         datetime(2022,  5, 29): 5,
         datetime(2022,  6,  1): 6,
         datetime(2022,  7,  1): 7,
         datetime(2022,  9,  5): 1,
         datetime(2022, 10, 12): 2,
         datetime(2022, 11, 27): 3,
         datetime(2022, 12, 10): 4,
         datetime(2023,  1, 14): 5,
         datetime(2023,  2, 21): 6,
         datetime(2023,  4, 30): 1,
      }
      for when in data: j.record("Test entry", when=when)
      del j
      time.sleep(0.1)

      j = Journal()
      persisted_streaks = [e.streak for e in j]

      self.assertListEqual(persisted_streaks, list(data.values()))

   def test_yearly_streak_checker(self):
      """
      Make sure YEARLY streak tracking works
      """
      j = Journal("Test journal", streak_mode=StreakCheck.YEARLY)

      data = {
         datetime(2007,  1, 1): 1,
         datetime(2008,  1, 1): 2,
         datetime(2008,  2, 1): 2,
         datetime(2008,  3, 1): 2,
         datetime(2008,  4, 1): 2,
         datetime(2008,  5, 1): 2,
         datetime(2008,  6, 1): 2,
         datetime(2008,  7, 1): 2,
         datetime(2008,  8, 1): 2,
         datetime(2008,  9, 1): 2,
         datetime(2008, 10, 1): 2,
         datetime(2008, 11, 1): 2,
         datetime(2008, 12, 1): 2,
         datetime(2009, 12, 1): 3,
         datetime(2010,  6, 1): 4,
         datetime(2012,  6, 1): 1,
         datetime(2013,  9, 1): 2,
      }
      for when in data: j.record("Test entry", when=when)
      del j
      time.sleep(0.1)

      j = Journal()
      persisted_streaks = [e.streak for e in j]

      self.assertListEqual(persisted_streaks, list(data.values()))

class TestTrackGoal(unittest.TestCase):
   """
   Make sure goal tracking works
   """
   def setUp(self):
      """Simple to-do list example
      """
      j = Journal("Test journal")

      actions = (
         (datetime(2023, 1, 1, 6, 0), "laundry", "TODO"),
         (datetime(2023, 1, 1, 6, 0), "groceries", "TODO"),
         (datetime(2023, 1, 1, 6, 0), "homework", "TODO"),
         (datetime(2023, 1, 1, 7, 0), "laundry", "DOING"),
         (datetime(2023, 1, 1, 7, 30), "homework", "DOING"),
         (datetime(2023, 1, 1, 9, 0), "homework", "CANCELED"),
         (datetime(2023, 1, 1, 9, 30), "laundry", "DONE"),
         (datetime(2023, 1, 1, 10, 0), "visit friends", "DOING"),
         (datetime(2023, 1, 1, 13, 0), "visit friends", "DONE"),
         (datetime(2023, 1, 1, 13, 30), "groceries", "DOING"),
         (datetime(2023, 1, 1, 14, 30), "groceries", "DONE"),
      )
      for when, name, state in actions: j.goal(name, state, when=when)
      time.sleep(0.1)

   def tearDown(self):
      """perform cleanup after each test
      """
      Path("journal.db").unlink(missing_ok=True)

   def test_goal_iterate(self):
      """Test if can iterate through Journal.goals
      """
      j = Journal()
      for g in j.goals(all=True):
         self.assertIsInstance(g, Goal)
         self.assertIsInstance(g.when, datetime)

      self.assertEqual(len(list(j.goals())), 4)
      self.assertEqual(len(list(j.goals(all=True))), 11)

   def test_goal_state_tracking(self):
      """Track goal states
      """
      j = Journal()

      self.assertEqual(j.goal("laundry").state, "DONE")
      self.assertEqual(j.goal("homework").state, "CANCELED")
      self.assertEqual(j.goal("groceries", when=datetime(2023, 1, 1, 10, 0)).state, "TODO")
      self.assertEqual(j.goal("visit friends", when=datetime(2023, 1, 1, 10, 0)).state, "DOING")
      self.assertEqual(j.goal("visit friends", when=datetime(2023, 1, 1, 12, 59)).state, "DOING")
      self.assertEqual(j.goal("visit friends", when=datetime(2023, 1, 1, 13, 0)).state, "DONE")
      with self.assertRaises(ZeroEntriesFound):
         j.goal("visit friends", when=datetime(2023, 1, 1, 6, 0))

   def test_goal_time_tracking(self):
      """Track goal times with simple to-do list example
      """
      j = Journal()

      self.assertEqual(j.time_in_state("laundry", "DOING"), timedelta(hours=2, minutes=30))
      self.assertEqual(j.time_in_state("groceries", "DOING"), timedelta(hours=1))
      self.assertEqual(j.time_in_state("homework", "DOING"), timedelta(hours=1, minutes=30))
      self.assertEqual(j.time_in_state("visit friends", "DOING"), timedelta(hours=3))
