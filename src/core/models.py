from dataclasses import dataclass
from typing import Optional

@dataclass
class Odds:
    home: float
    away: float
    draw: float

@dataclass
class Match:
    id: str
    home_team: str
    away_team: str
    odds: Optional[Odds] = None
