
import argparse
from pathlib import Path
from datetime import datetime

import perennial

def _parse_path(arg: str) -> Path:
   return Path(arg)

def _parse_date(arg: str) -> datetime:
   try:
      when = datetime.strptime(arg, "%Y-%m-%d")
   except ValueError:
      raise argparse.ArgumentTypeError
   return when

def _parse_streak_mode(arg: str) -> perennial.StreakCheck:
   try:
      streak_mode = perennial.StreakCheck(arg)
   except AttributeError:
      raise argparse.ArgumentTypeError
   return streak_mode

def parse_args():
   # Top level parser
   parser = argparse.ArgumentParser(
      prog="python -m perennial",
      description="Journaling kit for long-term self-analysis."
   )
   parser.add_argument("-d", "--database", type=_parse_path, help=(
      "Path to the journal's SQLite database or the directory that contains "
      "the database. If not provided, uses current working directory."
   ))
   
   # Add the subcommand subparsers
   sub_parsers = parser.add_subparsers(title="commands", dest="sub")

   # init command
   init_parser = sub_parsers.add_parser("init", help="Start a new journal.")
   init_parser.add_argument("content", type=str, help="Journal summary.")
   init_parser.add_argument("-s", "--streak-mode", type=_parse_streak_mode, default=perennial.StreakCheck.WEEKLY,
         help='Streak mode ("daily", "weekly", "monthly", or "yearly"). Default is weekly.')
   init_parser.add_argument("-t", "--template", type=_parse_path, help="Template file to use for new journal entries.")

   # record command
   record_parser = sub_parsers.add_parser("record", help="Record a journal entry.")
   record_parser.add_argument("content", type=str, help="Journal entry summary.")
   record_parser.add_argument("-m", "--mood", type=int, help="Mood level (e.g. on a scale 1-5).")
   record_parser.add_argument("-w", "--when", type=_parse_date, help="Date of journal entry, yyyy-mm-dd. If not provided, uses today's date.")
   record_parser.add_argument("-f", "--file", type=_parse_path, help="Path to the entry's associated file. Created if it doesn't already exist.")

   # goal command
   goal_parser = sub_parsers.add_parser("goal", help="Update the status of a goal.")
   goal_parser.add_argument("name", type=str, help="Name of the goal. Must be exact.")
   goal_parser.add_argument("state", type=str, default="TODO", help='State of the goal. Default is "TODO".')

   # about command
   about_parser = sub_parsers.add_parser("check", help="Check info about the journal.")

   # Parse the arguments
   args = parser.parse_args()

   return args

def initialize_journal(args: argparse.Namespace):
   """Create a new journal
   """
   journal = perennial.Journal(
      args.content,
      file=args.database,
      streak_mode=args.streak_mode,
      template=args.template,
   )
   print(f"Created new journal {journal.content!r} successfully.")

def record_entry(args: argparse.Namespace):
   """Record a journal entry
   """
   journal = perennial.Journal(file=args.database)
   entry = journal.record(
      args.content,
      mood=args.mood,
      when=args.when,
      file=args.file,
   )
   print(f"Created new entry {entry.content!r} successfully.")

def about_journal(args: argparse.Namespace):
   """Get info about the journal
   """
   path = args.database if args.database is not None else Path.cwd()
   if path.name != "journal.db": path /= "journal.db"
   if not path.exists():
      print(f"Journal {path!r} not found. You can create it with the init command.")
      return

   journal = perennial.Journal(file=path)

   num_goals = len(list(journal.goals()))

   print(journal.content)
   print("=" * len(journal.content))
   print()
   print(f"   file:          {journal.file}")
   print(f"   created:       {journal.when}")
   print(f"   streak mode:   {journal.streak_mode.value}")
   print(f"   template:      {journal.template}")
   print(f"   entries:       {len(journal)}")
   print(f"   streak:        {journal.streak()}")
   print(f"   goals:         {num_goals}")
   print()
   if num_goals:
      print("Goals")
      print("-----")
      print()
      for goal in journal.goals():
         spacing = " " * max(0, 14 - len(repr(goal.name)))
         print(f"   {goal.name!r}:{spacing}{goal.state!r} ({goal.when})")
      print()

def update_goal(args: argparse.Namespace):
   """Change the status of a goal
   """
   journal = perennial.Journal(file=args.database)
   goal = journal.goal(args.name, args.state)
   print(f"Updated goal {goal.name!r} with state {goal.state!r}.")

handlers = {
   "init": initialize_journal,
   "record": record_entry,
   "check": about_journal,
   "goal": update_goal,
}

if __name__ == "__main__":
   args = parse_args()
   #for k, v in args.__dict__.items(): print(f"   {k} -> {v}")

   if args.sub in handlers:
      handlers[args.sub](args)
