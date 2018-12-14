import datetime
from pathlib import Path
from typing import Dict

from bs4 import BeautifulSoup

import models


def set_match_attr(match: models.Match, key: str, value: str):
    key = key.lower().replace(' ', '_')

    field_type = models.MATCH_FIELDS[key]
    if value is None or value == 'None' or (field_type is not str and value.strip() == ''):
        value = None
    elif field_type is int:
        value = int(value)
    elif field_type is bool:
        value = (value.lower() == 'yes')
    elif field_type is datetime.datetime:
        value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S %Z')

    setattr(match, key, value)


def compress(matches: Dict[int, models.Match]) -> models.Result:
    result = models.Result()

    result.current_rating = list(matches.values())[0].result_displayed_rating

    for match_id in matches:
        match = matches[match_id]
        if not match.reached_conclusion:
            continue
        if match.type == 'Competitive':
            continue

        result.matches_played += 1

        if match.result_displayed_rating is not None:
            if match.result_displayed_rating > result.max_rating:
                result.max_rating = match.result_displayed_rating
            elif match.result_displayed_rating < result.min_rating:
                result.min_rating = match.result_displayed_rating

        if match.result_team is not None and match.winning_team is not None:
            if match.winning_team == match.result_team:
                result.wins += 1
                result.rating_won += match.result_displayed_rating_change
                if not match.result_displayed_rating_change:
                    result.zero_rating_wins += 1
            else:
                result.losses += 1
                result.rating_lost += match.result_displayed_rating_change
                if not match.result_displayed_rating_change:
                    result.zero_rating_losses += 1

        if match.damage is not None:
            result.total_damage += match.damage
        if match.healing is not None:
            result.total_healing += match.healing

    result.ratio = result.wins / result.matches_played
    result.avg_rating_won = result.rating_won / result.matches_played
    result.avg_rating_lost = result.rating_lost / result.matches_played
    result.zero_rating_wins_ratio = result.zero_rating_wins / result.wins
    result.zero_rating_losses_ratio = result.zero_rating_losses / result.losses
    return result


def main() -> models.Result:
    matches = {}
    for path in Path('.').glob('*.log'):
        content = path.read_text()
        soup = BeautifulSoup(content, 'lxml')
        print(f'{len(soup.find_all("table"))} matches')
        for table in soup.find_all('table'):
            match = models.Match()
            set_match_attr(match, 'id', table.tr.th.string.split(' ')[1])
            data = table.find_all('td')
            for key, value in zip(data[::2], data[1::2]):
                set_match_attr(match, str(key.string), str(value.string))
            if match.id in matches:
                print(f'ID {match.id} already set')
            matches[match.id] = match

    return compress(matches)


if __name__ == '__main__':
    print(main())
