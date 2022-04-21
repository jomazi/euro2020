from datetime import date, datetime, timezone
from typing import List

import pandas as pd

from .team import get_teams


def get_schedule(dt_index: bool = False) -> pd.DataFrame:
    schedule = pd.read_csv("./data/schedule.csv", header=0, sep=",")

    if dt_index:
        schedule.index = pd.to_datetime(schedule.datetime_utc, utc=True)    # convert to datetime index
        schedule.drop("datetime_utc", axis=1, inplace=True)

    return schedule


def get_playing_teams(start: datetime, stop: datetime, with_acronyms: bool = True) -> List[str]:
    assert start.tzinfo == timezone.utc and stop.tzinfo == timezone.utc, "start and stop datetimes should be given in UTC"

    # schedule of competition
    schedule = get_schedule(dt_index=True)

    # soccer teams
    teams = get_teams()

    # extend by team acronyms
    if with_acronyms:
        schedule = schedule.join(teams, on="team_1").join(teams, on="team_2", rsuffix="_team_2")
        schedule.rename(columns={"acronym": "team_1_acronym", "acronym_team_2": "team_2_acronym"}, inplace=True)

    # select playing teams based on schedule
    selected_schedule = schedule.loc[(schedule.index >= start) & (schedule.index < stop)]
    playing_teams = []
    [playing_teams.extend(s) for s in selected_schedule.values.tolist()]

    return playing_teams


def get_match_times_by_acronym(acronym: str) -> List[datetime]:
    # soccer teams
    teams = get_teams(acronym_idx=True)
    team_name = teams.loc[acronym].full_name

    # schedule
    schedule = get_schedule()
    schedule_filtered = schedule.loc[(schedule["team_1"] == team_name) | (
        schedule["team_2"] == team_name), ["datetime_utc"]]

    return list(pd.to_datetime(schedule_filtered.datetime_utc, utc=True))


def get_opponents(acronym: str) -> List[str]:
    # teams
    teams = get_teams(acronym_idx=True)
    team_name = teams.loc[acronym].full_name

    # schedule
    schedule = get_schedule()
    filter1 = schedule.loc[schedule["team_1"] == team_name, ["team_2", "datetime_utc"]]
    filter1.rename(columns={"team_2": "team"}, inplace=True)
    filter2 = schedule.loc[schedule["team_2"] == team_name, ["team_1", "datetime_utc"]]
    filter2.rename(columns={"team_1": "team"}, inplace=True)

    # filter schedule to get opponents
    schedule_filtered = pd.concat([filter1, filter2], ignore_index=True)
    teams.reset_index(inplace=True)
    teams.set_index("full_name", inplace=True)
    schedule_filtered = schedule_filtered.join(teams, on="team")
    schedule_filtered.sort_values(by=["datetime_utc"], inplace=True)

    return list(schedule_filtered["acronym"])


def last_group_stage_day() -> date:
    dt = datetime(year=2021, month=6, day=23)

    return dt.date()


def day_before_tournament() -> date:
    dt = datetime(year=2021, month=6, day=10)

    return dt.date()
