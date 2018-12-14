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
        result.matches_played += 1

        if match.result_displayed_rating > result.max_rating:
            result.max_rating = match.result_displayed_rating
        elif match.result_displayed_rating < result.min_rating:
            result.min_rating = match.result_displayed_rating

        result.total_damage += match.damage
        result.total_healing += match.healing

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
