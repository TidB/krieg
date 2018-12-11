import dataclasses
import datetime
from pathlib import Path
import re

from bs4 import BeautifulSoup

@dataclasses.dataclass
class Match:
    id: int
    conclusion: bool
    type: str
    map_index: int
    creation_time: datetime.datetime
    ip: str
    port: int
    datacenter: int
    size: int
    join_time: datetime.datetime
    join_party_id: int
    join_team: int
    ping_estimate: int
    joined_late: bool
    queue_time: int
    end: datetime.datetime
    season_id: int
    status: int
    duration: datetime.timedelta
    red_score: int
    blu_score: int
    winners: int
    mode: int
    win_reason: int
    flags: int
    had_bots: int
    left: datetime.datetime
    result_party_id: int
    result_team: int
    result_score: int
    result_ping: int
    result_flags: int
    result_rating: int
    result_rating_change: int
    result_rank: int
    classes_played: int
    kills: int
    deaths: int
    damage: int
    healing: int
    support: int
    score_medal: int
    kills_medal: int
    damage_medal: int
    healing_medal: int
    support_medal: int
    leave_reason: int
    connection_time: datetime.datetime


def main():
    for path in Path('.').glob('*.log'):
        content = path.read_text()
        content = re.sub('Script snippet %\d+?:\d+ ', '', content)

        html = BeautifulSoup(content, 'html.parser')

if __name__ == '__main__':
    main()
