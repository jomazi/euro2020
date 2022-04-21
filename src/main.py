import argparse
from datetime import date, datetime, timedelta, timezone
from typing import List

from euro2020 import (day_before_tournament, get_all_acronyms,
                      get_match_times_by_acronym, get_opponents,
                      get_playing_teams, last_group_stage_day)
from twitter import search_tweets

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--twitter", help="collect Twitter data", action="store_true")
    parser.add_argument("--euro2020", help="get EURO2020 information", action="store_true")

    args = parser.parse_args()

    # run task requested by user
    if args.twitter:
        search_tweets()
    elif args.euro2020:
        # schedule related information
        day_before: date = day_before_tournament()
        print("Day before tournament:\n", day_before)
        first_day: date = day_before + timedelta(days=1)
        first_day: datetime = datetime(year=first_day.year, month=first_day.month,
                                       day=first_day.day, tzinfo=timezone.utc)
        second_day: datetime = first_day + timedelta(days=1)
        print("\nTeams playing at first day of tournament:\n", get_playing_teams(
            start=first_day, stop=second_day, with_acronyms=False))
        print("\nMatch times of Germany:\n", get_match_times_by_acronym(acronym="GER"))
        print("\nOpponents of German team:\n", get_opponents(acronym="GER"))
        print("\nLast day of group stage:\n", last_group_stage_day())
        # teams related information
        acronyms: List[str] = get_all_acronyms()
        print("\nAcronyms of teams:\n", acronyms)
        print("\nNumber of participating teams:\n", len(acronyms))
