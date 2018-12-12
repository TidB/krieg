import dataclasses
import datetime
import json
from pathlib import Path

from bs4 import BeautifulSoup


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif isinstance(o, datetime.datetime):
            return datetime.datetime.isoformat(o)
        return super().default(o)


@dataclasses.dataclass(init=False)
class Match:
    id: int
    reached_conclusion: bool
    type: str
    map_index: int
    match_creation_time: datetime.datetime
    match_ip: str
    match_port: int
    datacenter: str
    match_size: int
    join_time: datetime.datetime
    party_id_at_join: int
    team_at_join: int
    ping_estimate_at_join: int
    joined_after_match_start: bool
    time_in_queue: int
    match_end_time: datetime.datetime = None
    season_id: int = None
    match_status: int = None
    match_duration: int = None
    red_team_final_score: int = None
    blu_team_final_score: int = None
    winning_team: int = None
    game_mode: int = None
    win_reason: int = None
    match_flags: int = None
    match_included_bots: int = None
    time_left_match: datetime.datetime = None
    result_partyid: int = None
    result_team: int = None
    result_score: int = None
    result_ping: int = None
    result_player_flags: int = None
    result_displayed_rating: int = None
    result_displayed_rating_change: int = None
    result_rank: int = None
    classes_played: int = None
    kills: int = None
    deaths: int = None
    damage: int = None
    healing: int = None
    support: int = None
    score_medal: int = None
    kills_medal: int = None
    damage_medal: int = None
    healing_medal: int = None
    support_medal: int = None
    leave_reason: int = None
    connection_time: datetime.datetime = None


MATCH_FIELDS = {field.name: field.type for field in dataclasses.fields(Match)}


def set_match_attr(match: Match, key: str, value: str):
    key = key.lower().replace(' ', '_')

    field_type = MATCH_FIELDS[key]
    if value is None or value == 'None' or (field_type is not str and value.strip() == ''):
        value = None
    elif field_type is int:
        value = int(value)
    elif field_type is bool:
        value = (value.lower() == 'yes')
    elif field_type is datetime.datetime:
        value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S %Z')

    setattr(match, key, value)


def main():
    matches = {}
    for path in Path('.').glob('*.log'):
        content = path.read_text()
        soup = BeautifulSoup(content, 'lxml')
        print(f'{len(soup.find_all("table"))} matches')
        for table in soup.find_all('table'):
            match = Match()
            set_match_attr(match, 'id', table.tr.th.string.split(' ')[1])
            data = table.find_all('td')
            for key, value in zip(data[::2], data[1::2]):
                set_match_attr(match, str(key.string), str(value.string))
            if match.id in matches:
                print(f'ID {match.id} already set')
            matches[match.id] = match

    Path('parsed.json').write_text(json.dumps(matches, cls=EnhancedJSONEncoder))


if __name__ == '__main__':
    main()
