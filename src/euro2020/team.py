from typing import List

import pandas as pd


def get_all_acronyms() -> List[str]:
    teams = pd.read_csv("./data/teams.csv", header=0, sep=",", index_col=0)

    return list(set(teams.acronym))


def get_teams(acronym_idx: bool = False) -> pd.DataFrame:
    if acronym_idx:
        return pd.read_csv("./data/teams.csv", header=0, sep=",", index_col=1)
    else:
        return pd.read_csv("./data/teams.csv", header=0, sep=",", index_col=0)
