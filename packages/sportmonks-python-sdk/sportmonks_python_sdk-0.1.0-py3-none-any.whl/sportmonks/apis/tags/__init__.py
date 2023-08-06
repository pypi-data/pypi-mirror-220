# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from sportmonks.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    SPORT = "Sport"
    ODDS = "Odds"
    COUNTRIES = "Countries"
    REGIONS = "Regions"
    CITIES = "Cities"
    MY = "My"
    CONTINENTS = "Continents"
    TYPES = "Types"
    CORE = "Core"
    FOOTBALL = "Football"
