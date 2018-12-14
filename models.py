import dataclasses
import datetime


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


@dataclasses.dataclass
class Result:
    matches_played: int = 0

    wins: int = 0
    losses: int = 0
    ratio: float = 0.0

    rating_won: int = 0
    rating_lost: int = 0
    avg_rating_won: float = 0.0
    avg_rating_lost: float = 0.0
    zero_rating_wins: int = 0
    zero_rating_losses: int = 0
    zero_rating_wins_ratio: float = 0.0
    zero_rating_losses_ratio: float = 0.0

    current_rating: int = 0
    min_rating: int = 5000
    max_rating: int = 0
    total_damage: int = 0
    total_healing: int = 0