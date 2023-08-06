import typing_extensions

from sportmonks.apis.tags import TagValues
from sportmonks.apis.tags.sport_api import SportApi
from sportmonks.apis.tags.odds_api import OddsApi
from sportmonks.apis.tags.countries_api import CountriesApi
from sportmonks.apis.tags.regions_api import RegionsApi
from sportmonks.apis.tags.cities_api import CitiesApi
from sportmonks.apis.tags.my_api import MyApi
from sportmonks.apis.tags.continents_api import ContinentsApi
from sportmonks.apis.tags.types_api import TypesApi
from sportmonks.apis.tags.core_api import CoreApi
from sportmonks.apis.tags.football_api import FootballApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.SPORT: SportApi,
        TagValues.ODDS: OddsApi,
        TagValues.COUNTRIES: CountriesApi,
        TagValues.REGIONS: RegionsApi,
        TagValues.CITIES: CitiesApi,
        TagValues.MY: MyApi,
        TagValues.CONTINENTS: ContinentsApi,
        TagValues.TYPES: TypesApi,
        TagValues.CORE: CoreApi,
        TagValues.FOOTBALL: FootballApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.SPORT: SportApi,
        TagValues.ODDS: OddsApi,
        TagValues.COUNTRIES: CountriesApi,
        TagValues.REGIONS: RegionsApi,
        TagValues.CITIES: CitiesApi,
        TagValues.MY: MyApi,
        TagValues.CONTINENTS: ContinentsApi,
        TagValues.TYPES: TypesApi,
        TagValues.CORE: CoreApi,
        TagValues.FOOTBALL: FootballApi,
    }
)
