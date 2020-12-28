from fastapi import Query
from enum import Enum
from pydantic import BaseModel, constr
from typing import List, Dict, Any
from datetime import datetime


class TargetType(str, Enum):
    line = 'line',
    zone = 'zone',
    stop = 'stop'

class TicketType(str, Enum):
    GDBILET = "GDBILET"
    BILET = "BILET"
    TBILET = "TBILET"
    KBILET = "KBILET"
    GBILET = "GBILET"
    ABILET = "ABILET"
    GLBILET = "GLBILET"


class ReportParams:
    def __init__(self,
                 # Source for the regex below https://www.regextester.com/96683
                 date: List[constr(regex="([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))")] = Query(None, description="List of dates to be analyzed. Must be in the format of 2020-06-17"),
                 preview: bool = Query(False),
                 line: List[int] = Query(None),
                 stop: List[str] = Query(None),
                 ticket: List[TicketType] = Query(None),
                 start_hour: constr(regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$") = Query(None, description="Start time"),
                 end_hour: constr(regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$") = Query(None, description="End time"),
                ):
        self.date = date
        self.preview = preview
        self.line = line
        self.stop = stop
        self.ticket = ticket
        self.start_hour = start_hour
        self.end_hour = end_hour

