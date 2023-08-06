import typing_extensions

from sportmonks.paths import PathValues
from sportmonks.apis.paths.version_core_continents import VersionCoreContinents
from sportmonks.apis.paths.version_core_continents_continent_id import VersionCoreContinentsContinentId
from sportmonks.apis.paths.version_core_countries import VersionCoreCountries
from sportmonks.apis.paths.version_core_countries_country_id import VersionCoreCountriesCountryId
from sportmonks.apis.paths.version_core_countries_search_name import VersionCoreCountriesSearchName
from sportmonks.apis.paths.version_core_regions import VersionCoreRegions
from sportmonks.apis.paths.version_core_regions_region_id import VersionCoreRegionsRegionId
from sportmonks.apis.paths.version_core_regions_search_name import VersionCoreRegionsSearchName
from sportmonks.apis.paths.version_core_cities import VersionCoreCities
from sportmonks.apis.paths.version_core_cities_city_id import VersionCoreCitiesCityId
from sportmonks.apis.paths.version_core_cities_search_name import VersionCoreCitiesSearchName
from sportmonks.apis.paths.version_core_types import VersionCoreTypes
from sportmonks.apis.paths.version_core_types_type_id import VersionCoreTypesTypeId
from sportmonks.apis.paths.version_sport_leagues import VersionSportLeagues
from sportmonks.apis.paths.version_sport_leagues_live import VersionSportLeaguesLive
from sportmonks.apis.paths.version_sport_leagues_league_id import VersionSportLeaguesLeagueId
from sportmonks.apis.paths.version_sport_leagues_league_id_jerseys import VersionSportLeaguesLeagueIdJerseys
from sportmonks.apis.paths.version_sport_leagues_league_id_includes import VersionSportLeaguesLeagueIdIncludes
from sportmonks.apis.paths.version_sport_leagues_date_date import VersionSportLeaguesDateDate
from sportmonks.apis.paths.version_sport_leagues_countries_country_id import VersionSportLeaguesCountriesCountryId
from sportmonks.apis.paths.version_sport_leagues_search_name import VersionSportLeaguesSearchName
from sportmonks.apis.paths.version_sport_fixtures import VersionSportFixtures
from sportmonks.apis.paths.version_sport_fixtures_latest import VersionSportFixturesLatest
from sportmonks.apis.paths.version_sport_fixtures_fixture_id import VersionSportFixturesFixtureId
from sportmonks.apis.paths.version_sport_fixtures_search_name import VersionSportFixturesSearchName
from sportmonks.apis.paths.version_sport_fixtures_date_date import VersionSportFixturesDateDate
from sportmonks.apis.paths.version_sport_fixtures_multi_fixture_ids import VersionSportFixturesMultiFixtureIds
from sportmonks.apis.paths.version_sport_fixtures_between_start_date_end_date import VersionSportFixturesBetweenStartDateEndDate
from sportmonks.apis.paths.version_sport_fixtures_between_start_date_end_date_team_id import VersionSportFixturesBetweenStartDateEndDateTeamId
from sportmonks.apis.paths.version_sport_fixtures_head_to_head_first_team_second_team import VersionSportFixturesHeadToHeadFirstTeamSecondTeam
from sportmonks.apis.paths.version_sport_livescores_latest import VersionSportLivescoresLatest
from sportmonks.apis.paths.version_sport_livescores import VersionSportLivescores
from sportmonks.apis.paths.version_sport_livescores_inplay import VersionSportLivescoresInplay
from sportmonks.apis.paths.version_sport_teams import VersionSportTeams
from sportmonks.apis.paths.version_sport_teams_countries_country_id import VersionSportTeamsCountriesCountryId
from sportmonks.apis.paths.version_sport_teams_seasons_season_id import VersionSportTeamsSeasonsSeasonId
from sportmonks.apis.paths.version_sport_teams_search_name import VersionSportTeamsSearchName
from sportmonks.apis.paths.version_sport_teams_team_id import VersionSportTeamsTeamId
from sportmonks.apis.paths.version_sport_teams_team_id_leagues import VersionSportTeamsTeamIdLeagues
from sportmonks.apis.paths.version_sport_teams_team_id_leagues_current import VersionSportTeamsTeamIdLeaguesCurrent
from sportmonks.apis.paths.version_sport_standings import VersionSportStandings
from sportmonks.apis.paths.version_sport_standings_seasons_season_id import VersionSportStandingsSeasonsSeasonId
from sportmonks.apis.paths.version_sport_standings_rounds_round_id import VersionSportStandingsRoundsRoundId
from sportmonks.apis.paths.version_sport_standings_corrections_seasons_season_id import VersionSportStandingsCorrectionsSeasonsSeasonId
from sportmonks.apis.paths.version_sport_standings_live_leagues_league_id import VersionSportStandingsLiveLeaguesLeagueId
from sportmonks.apis.paths.version_sport_schedules_seasons_season_id import VersionSportSchedulesSeasonsSeasonId
from sportmonks.apis.paths.version_sport_schedules_seasons_season_id_teams_team_id import VersionSportSchedulesSeasonsSeasonIdTeamsTeamId
from sportmonks.apis.paths.version_sport_schedules_teams_team_id import VersionSportSchedulesTeamsTeamId
from sportmonks.apis.paths.version_sport_players import VersionSportPlayers
from sportmonks.apis.paths.version_sport_players_latest import VersionSportPlayersLatest
from sportmonks.apis.paths.version_sport_players_player_id import VersionSportPlayersPlayerId
from sportmonks.apis.paths.version_sport_players_countries_country_id import VersionSportPlayersCountriesCountryId
from sportmonks.apis.paths.version_sport_players_search_name import VersionSportPlayersSearchName
from sportmonks.apis.paths.version_sport_news_pre_match import VersionSportNewsPreMatch
from sportmonks.apis.paths.version_sport_news_pre_match_seasons_season_id import VersionSportNewsPreMatchSeasonsSeasonId
from sportmonks.apis.paths.version_sport_news_pre_match_upcoming import VersionSportNewsPreMatchUpcoming
from sportmonks.apis.paths.version_sport_news_post_match import VersionSportNewsPostMatch
from sportmonks.apis.paths.version_sport_news_post_match_seasons_season_id import VersionSportNewsPostMatchSeasonsSeasonId
from sportmonks.apis.paths.version_sport_news_post_match_upcoming import VersionSportNewsPostMatchUpcoming
from sportmonks.apis.paths.version_sport_venues import VersionSportVenues
from sportmonks.apis.paths.version_sport_venues_venue_id import VersionSportVenuesVenueId
from sportmonks.apis.paths.version_sport_venues_search_name import VersionSportVenuesSearchName
from sportmonks.apis.paths.version_sport_venues_seasons_season_id import VersionSportVenuesSeasonsSeasonId
from sportmonks.apis.paths.version_sport_seasons import VersionSportSeasons
from sportmonks.apis.paths.version_sport_seasons_season_id import VersionSportSeasonsSeasonId
from sportmonks.apis.paths.version_sport_seasons_teams_team_id import VersionSportSeasonsTeamsTeamId
from sportmonks.apis.paths.version_sport_seasons_search_name import VersionSportSeasonsSearchName
from sportmonks.apis.paths.version_sport_squads_teams_team_id import VersionSportSquadsTeamsTeamId
from sportmonks.apis.paths.version_sport_squads_seasons_season_id_teams_team_id import VersionSportSquadsSeasonsSeasonIdTeamsTeamId
from sportmonks.apis.paths.version_sport_tv_stations import VersionSportTvStations
from sportmonks.apis.paths.version_sport_tv_stations_tv_station_id import VersionSportTvStationsTvStationId
from sportmonks.apis.paths.version_sport_tv_stations_fixtures_fixture_id import VersionSportTvStationsFixturesFixtureId
from sportmonks.apis.paths.version_sport_coaches import VersionSportCoaches
from sportmonks.apis.paths.version_sport_coaches_latest import VersionSportCoachesLatest
from sportmonks.apis.paths.version_sport_coaches_coach_id import VersionSportCoachesCoachId
from sportmonks.apis.paths.version_sport_coaches_countries_country_id import VersionSportCoachesCountriesCountryId
from sportmonks.apis.paths.version_sport_coaches_search_name import VersionSportCoachesSearchName
from sportmonks.apis.paths.version_sport_topscorers_stages_stage_id import VersionSportTopscorersStagesStageId
from sportmonks.apis.paths.version_sport_topscorers_seasons_season_id import VersionSportTopscorersSeasonsSeasonId
from sportmonks.apis.paths.version_sport_rounds import VersionSportRounds
from sportmonks.apis.paths.version_sport_rounds_round_id import VersionSportRoundsRoundId
from sportmonks.apis.paths.version_sport_rounds_search_name import VersionSportRoundsSearchName
from sportmonks.apis.paths.version_sport_rounds_seasons_season_id import VersionSportRoundsSeasonsSeasonId
from sportmonks.apis.paths.version_sport_stages import VersionSportStages
from sportmonks.apis.paths.version_sport_stages_stage_id import VersionSportStagesStageId
from sportmonks.apis.paths.version_sport_stages_search_name import VersionSportStagesSearchName
from sportmonks.apis.paths.version_sport_stages_seasons_season_id import VersionSportStagesSeasonsSeasonId
from sportmonks.apis.paths.version_sport_rivals import VersionSportRivals
from sportmonks.apis.paths.version_sport_rivals_teams_team_id import VersionSportRivalsTeamsTeamId
from sportmonks.apis.paths.version_sport_commentaries import VersionSportCommentaries
from sportmonks.apis.paths.version_sport_commentaries_fixtures_fixture_id import VersionSportCommentariesFixturesFixtureId
from sportmonks.apis.paths.version_sport_referees import VersionSportReferees
from sportmonks.apis.paths.version_sport_referees_referee_id import VersionSportRefereesRefereeId
from sportmonks.apis.paths.version_sport_referees_seasons_season_id import VersionSportRefereesSeasonsSeasonId
from sportmonks.apis.paths.version_sport_referees_countries_country_id import VersionSportRefereesCountriesCountryId
from sportmonks.apis.paths.version_sport_referees_search_name import VersionSportRefereesSearchName
from sportmonks.apis.paths.version_sport_transfers import VersionSportTransfers
from sportmonks.apis.paths.version_sport_transfers_latest import VersionSportTransfersLatest
from sportmonks.apis.paths.version_sport_transfers_transfer_id import VersionSportTransfersTransferId
from sportmonks.apis.paths.version_sport_transfers_between_start_date_end_date import VersionSportTransfersBetweenStartDateEndDate
from sportmonks.apis.paths.version_sport_transfers_teams_team_id import VersionSportTransfersTeamsTeamId
from sportmonks.apis.paths.version_sport_transfers_players_player_id import VersionSportTransfersPlayersPlayerId
from sportmonks.apis.paths.version_sport_states import VersionSportStates
from sportmonks.apis.paths.version_sport_states_state_id import VersionSportStatesStateId
from sportmonks.apis.paths.version_sport_predictions_probabilities import VersionSportPredictionsProbabilities
from sportmonks.apis.paths.version_sport_predictions_probabilities_fixtures_fixture_id import VersionSportPredictionsProbabilitiesFixturesFixtureId
from sportmonks.apis.paths.version_sport_predictions_value_bets import VersionSportPredictionsValueBets
from sportmonks.apis.paths.version_sport_predictions_value_bets_fixtures_fixture_id import VersionSportPredictionsValueBetsFixturesFixtureId
from sportmonks.apis.paths.version_sport_odds_pre_match import VersionSportOddsPreMatch
from sportmonks.apis.paths.version_sport_odds_pre_match_latest import VersionSportOddsPreMatchLatest
from sportmonks.apis.paths.version_sport_odds_pre_match_fixtures_fixture_id import VersionSportOddsPreMatchFixturesFixtureId
from sportmonks.apis.paths.version_sport_odds_pre_match_fixtures_fixture_id_bookmakers_bookmaker_id import VersionSportOddsPreMatchFixturesFixtureIdBookmakersBookmakerId
from sportmonks.apis.paths.version_sport_odds_pre_match_fixtures_fixture_id_markets_market_id import VersionSportOddsPreMatchFixturesFixtureIdMarketsMarketId
from sportmonks.apis.paths.version_sport_odds_inplay import VersionSportOddsInplay
from sportmonks.apis.paths.version_sport_odds_inplay_latest import VersionSportOddsInplayLatest
from sportmonks.apis.paths.version_sport_odds_inplay_fixtures_fixture_id import VersionSportOddsInplayFixturesFixtureId
from sportmonks.apis.paths.version_sport_odds_inplay_fixtures_fixture_id_bookmakers_bookmaker_id import VersionSportOddsInplayFixturesFixtureIdBookmakersBookmakerId
from sportmonks.apis.paths.version_sport_odds_inplay_fixtures_fixture_id_markets_market_id import VersionSportOddsInplayFixturesFixtureIdMarketsMarketId
from sportmonks.apis.paths.version_my_enrichments import VersionMyEnrichments
from sportmonks.apis.paths.version_my_resources import VersionMyResources
from sportmonks.apis.paths.version_my_leagues import VersionMyLeagues
from sportmonks.apis.paths.version_odds_markets import VersionOddsMarkets
from sportmonks.apis.paths.version_odds_markets_market_id import VersionOddsMarketsMarketId
from sportmonks.apis.paths.version_odds_markets_search_name import VersionOddsMarketsSearchName
from sportmonks.apis.paths.version_sport_fixtures_upcoming_markets_market_id import VersionSportFixturesUpcomingMarketsMarketId
from sportmonks.apis.paths.version_odds_bookmakers import VersionOddsBookmakers
from sportmonks.apis.paths.version_odds_bookmakers_bookmaker_id import VersionOddsBookmakersBookmakerId
from sportmonks.apis.paths.version_odds_bookmakers_search_name import VersionOddsBookmakersSearchName
from sportmonks.apis.paths.version_odds_bookmakers_fixtures_fixture_id import VersionOddsBookmakersFixturesFixtureId
from sportmonks.apis.paths.version_odds_bookmakers_fixtures_fixture_id_mapping import VersionOddsBookmakersFixturesFixtureIdMapping

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.VERSION_CORE_CONTINENTS: VersionCoreContinents,
        PathValues.VERSION_CORE_CONTINENTS_CONTINENT_ID: VersionCoreContinentsContinentId,
        PathValues.VERSION_CORE_COUNTRIES: VersionCoreCountries,
        PathValues.VERSION_CORE_COUNTRIES_COUNTRY_ID: VersionCoreCountriesCountryId,
        PathValues.VERSION_CORE_COUNTRIES_SEARCH_NAME: VersionCoreCountriesSearchName,
        PathValues.VERSION_CORE_REGIONS: VersionCoreRegions,
        PathValues.VERSION_CORE_REGIONS_REGION_ID: VersionCoreRegionsRegionId,
        PathValues.VERSION_CORE_REGIONS_SEARCH_NAME: VersionCoreRegionsSearchName,
        PathValues.VERSION_CORE_CITIES: VersionCoreCities,
        PathValues.VERSION_CORE_CITIES_CITY_ID: VersionCoreCitiesCityId,
        PathValues.VERSION_CORE_CITIES_SEARCH_NAME: VersionCoreCitiesSearchName,
        PathValues.VERSION_CORE_TYPES: VersionCoreTypes,
        PathValues.VERSION_CORE_TYPES_TYPE_ID: VersionCoreTypesTypeId,
        PathValues.VERSION_SPORT_LEAGUES: VersionSportLeagues,
        PathValues.VERSION_SPORT_LEAGUES_LIVE: VersionSportLeaguesLive,
        PathValues.VERSION_SPORT_LEAGUES_LEAGUE_ID: VersionSportLeaguesLeagueId,
        PathValues.VERSION_SPORT_LEAGUES_LEAGUE_ID_JERSEYS: VersionSportLeaguesLeagueIdJerseys,
        PathValues.VERSION_SPORT_LEAGUES_LEAGUE_ID_INCLUDES: VersionSportLeaguesLeagueIdIncludes,
        PathValues.VERSION_SPORT_LEAGUES_DATE_DATE: VersionSportLeaguesDateDate,
        PathValues.VERSION_SPORT_LEAGUES_COUNTRIES_COUNTRY_ID: VersionSportLeaguesCountriesCountryId,
        PathValues.VERSION_SPORT_LEAGUES_SEARCH_NAME: VersionSportLeaguesSearchName,
        PathValues.VERSION_SPORT_FIXTURES: VersionSportFixtures,
        PathValues.VERSION_SPORT_FIXTURES_LATEST: VersionSportFixturesLatest,
        PathValues.VERSION_SPORT_FIXTURES_FIXTURE_ID: VersionSportFixturesFixtureId,
        PathValues.VERSION_SPORT_FIXTURES_SEARCH_NAME: VersionSportFixturesSearchName,
        PathValues.VERSION_SPORT_FIXTURES_DATE_DATE: VersionSportFixturesDateDate,
        PathValues.VERSION_SPORT_FIXTURES_MULTI_FIXTURE_IDS: VersionSportFixturesMultiFixtureIds,
        PathValues.VERSION_SPORT_FIXTURES_BETWEEN_START_DATE_END_DATE: VersionSportFixturesBetweenStartDateEndDate,
        PathValues.VERSION_SPORT_FIXTURES_BETWEEN_START_DATE_END_DATE_TEAM_ID: VersionSportFixturesBetweenStartDateEndDateTeamId,
        PathValues.VERSION_SPORT_FIXTURES_HEADTOHEAD_FIRST_TEAM_SECOND_TEAM: VersionSportFixturesHeadToHeadFirstTeamSecondTeam,
        PathValues.VERSION_SPORT_LIVESCORES_LATEST: VersionSportLivescoresLatest,
        PathValues.VERSION_SPORT_LIVESCORES: VersionSportLivescores,
        PathValues.VERSION_SPORT_LIVESCORES_INPLAY: VersionSportLivescoresInplay,
        PathValues.VERSION_SPORT_TEAMS: VersionSportTeams,
        PathValues.VERSION_SPORT_TEAMS_COUNTRIES_COUNTRY_ID: VersionSportTeamsCountriesCountryId,
        PathValues.VERSION_SPORT_TEAMS_SEASONS_SEASON_ID: VersionSportTeamsSeasonsSeasonId,
        PathValues.VERSION_SPORT_TEAMS_SEARCH_NAME: VersionSportTeamsSearchName,
        PathValues.VERSION_SPORT_TEAMS_TEAM_ID: VersionSportTeamsTeamId,
        PathValues.VERSION_SPORT_TEAMS_TEAM_ID_LEAGUES: VersionSportTeamsTeamIdLeagues,
        PathValues.VERSION_SPORT_TEAMS_TEAM_ID_LEAGUES_CURRENT: VersionSportTeamsTeamIdLeaguesCurrent,
        PathValues.VERSION_SPORT_STANDINGS: VersionSportStandings,
        PathValues.VERSION_SPORT_STANDINGS_SEASONS_SEASON_ID: VersionSportStandingsSeasonsSeasonId,
        PathValues.VERSION_SPORT_STANDINGS_ROUNDS_ROUND_ID: VersionSportStandingsRoundsRoundId,
        PathValues.VERSION_SPORT_STANDINGS_CORRECTIONS_SEASONS_SEASON_ID: VersionSportStandingsCorrectionsSeasonsSeasonId,
        PathValues.VERSION_SPORT_STANDINGS_LIVE_LEAGUES_LEAGUE_ID: VersionSportStandingsLiveLeaguesLeagueId,
        PathValues.VERSION_SPORT_SCHEDULES_SEASONS_SEASON_ID: VersionSportSchedulesSeasonsSeasonId,
        PathValues.VERSION_SPORT_SCHEDULES_SEASONS_SEASON_ID_TEAMS_TEAM_ID: VersionSportSchedulesSeasonsSeasonIdTeamsTeamId,
        PathValues.VERSION_SPORT_SCHEDULES_TEAMS_TEAM_ID: VersionSportSchedulesTeamsTeamId,
        PathValues.VERSION_SPORT_PLAYERS: VersionSportPlayers,
        PathValues.VERSION_SPORT_PLAYERS_LATEST: VersionSportPlayersLatest,
        PathValues.VERSION_SPORT_PLAYERS_PLAYER_ID: VersionSportPlayersPlayerId,
        PathValues.VERSION_SPORT_PLAYERS_COUNTRIES_COUNTRY_ID: VersionSportPlayersCountriesCountryId,
        PathValues.VERSION_SPORT_PLAYERS_SEARCH_NAME: VersionSportPlayersSearchName,
        PathValues.VERSION_SPORT_NEWS_PREMATCH: VersionSportNewsPreMatch,
        PathValues.VERSION_SPORT_NEWS_PREMATCH_SEASONS_SEASON_ID: VersionSportNewsPreMatchSeasonsSeasonId,
        PathValues.VERSION_SPORT_NEWS_PREMATCH_UPCOMING: VersionSportNewsPreMatchUpcoming,
        PathValues.VERSION_SPORT_NEWS_POSTMATCH: VersionSportNewsPostMatch,
        PathValues.VERSION_SPORT_NEWS_POSTMATCH_SEASONS_SEASON_ID: VersionSportNewsPostMatchSeasonsSeasonId,
        PathValues.VERSION_SPORT_NEWS_POSTMATCH_UPCOMING: VersionSportNewsPostMatchUpcoming,
        PathValues.VERSION_SPORT_VENUES: VersionSportVenues,
        PathValues.VERSION_SPORT_VENUES_VENUE_ID: VersionSportVenuesVenueId,
        PathValues.VERSION_SPORT_VENUES_SEARCH_NAME: VersionSportVenuesSearchName,
        PathValues.VERSION_SPORT_VENUES_SEASONS_SEASON_ID: VersionSportVenuesSeasonsSeasonId,
        PathValues.VERSION_SPORT_SEASONS: VersionSportSeasons,
        PathValues.VERSION_SPORT_SEASONS_SEASON_ID: VersionSportSeasonsSeasonId,
        PathValues.VERSION_SPORT_SEASONS_TEAMS_TEAM_ID: VersionSportSeasonsTeamsTeamId,
        PathValues.VERSION_SPORT_SEASONS_SEARCH_NAME: VersionSportSeasonsSearchName,
        PathValues.VERSION_SPORT_SQUADS_TEAMS_TEAM_ID: VersionSportSquadsTeamsTeamId,
        PathValues.VERSION_SPORT_SQUADS_SEASONS_SEASON_ID_TEAMS_TEAM_ID: VersionSportSquadsSeasonsSeasonIdTeamsTeamId,
        PathValues.VERSION_SPORT_TVSTATIONS: VersionSportTvStations,
        PathValues.VERSION_SPORT_TVSTATIONS_TV_STATION_ID: VersionSportTvStationsTvStationId,
        PathValues.VERSION_SPORT_TVSTATIONS_FIXTURES_FIXTURE_ID: VersionSportTvStationsFixturesFixtureId,
        PathValues.VERSION_SPORT_COACHES: VersionSportCoaches,
        PathValues.VERSION_SPORT_COACHES_LATEST: VersionSportCoachesLatest,
        PathValues.VERSION_SPORT_COACHES_COACH_ID: VersionSportCoachesCoachId,
        PathValues.VERSION_SPORT_COACHES_COUNTRIES_COUNTRY_ID: VersionSportCoachesCountriesCountryId,
        PathValues.VERSION_SPORT_COACHES_SEARCH_NAME: VersionSportCoachesSearchName,
        PathValues.VERSION_SPORT_TOPSCORERS_STAGES_STAGE_ID: VersionSportTopscorersStagesStageId,
        PathValues.VERSION_SPORT_TOPSCORERS_SEASONS_SEASON_ID: VersionSportTopscorersSeasonsSeasonId,
        PathValues.VERSION_SPORT_ROUNDS: VersionSportRounds,
        PathValues.VERSION_SPORT_ROUNDS_ROUND_ID: VersionSportRoundsRoundId,
        PathValues.VERSION_SPORT_ROUNDS_SEARCH_NAME: VersionSportRoundsSearchName,
        PathValues.VERSION_SPORT_ROUNDS_SEASONS_SEASON_ID: VersionSportRoundsSeasonsSeasonId,
        PathValues.VERSION_SPORT_STAGES: VersionSportStages,
        PathValues.VERSION_SPORT_STAGES_STAGE_ID: VersionSportStagesStageId,
        PathValues.VERSION_SPORT_STAGES_SEARCH_NAME: VersionSportStagesSearchName,
        PathValues.VERSION_SPORT_STAGES_SEASONS_SEASON_ID: VersionSportStagesSeasonsSeasonId,
        PathValues.VERSION_SPORT_RIVALS: VersionSportRivals,
        PathValues.VERSION_SPORT_RIVALS_TEAMS_TEAM_ID: VersionSportRivalsTeamsTeamId,
        PathValues.VERSION_SPORT_COMMENTARIES: VersionSportCommentaries,
        PathValues.VERSION_SPORT_COMMENTARIES_FIXTURES_FIXTURE_ID: VersionSportCommentariesFixturesFixtureId,
        PathValues.VERSION_SPORT_REFEREES: VersionSportReferees,
        PathValues.VERSION_SPORT_REFEREES_REFEREE_ID: VersionSportRefereesRefereeId,
        PathValues.VERSION_SPORT_REFEREES_SEASONS_SEASON_ID: VersionSportRefereesSeasonsSeasonId,
        PathValues.VERSION_SPORT_REFEREES_COUNTRIES_COUNTRY_ID: VersionSportRefereesCountriesCountryId,
        PathValues.VERSION_SPORT_REFEREES_SEARCH_NAME: VersionSportRefereesSearchName,
        PathValues.VERSION_SPORT_TRANSFERS: VersionSportTransfers,
        PathValues.VERSION_SPORT_TRANSFERS_LATEST: VersionSportTransfersLatest,
        PathValues.VERSION_SPORT_TRANSFERS_TRANSFER_ID: VersionSportTransfersTransferId,
        PathValues.VERSION_SPORT_TRANSFERS_BETWEEN_START_DATE_END_DATE: VersionSportTransfersBetweenStartDateEndDate,
        PathValues.VERSION_SPORT_TRANSFERS_TEAMS_TEAM_ID: VersionSportTransfersTeamsTeamId,
        PathValues.VERSION_SPORT_TRANSFERS_PLAYERS_PLAYER_ID: VersionSportTransfersPlayersPlayerId,
        PathValues.VERSION_SPORT_STATES: VersionSportStates,
        PathValues.VERSION_SPORT_STATES_STATE_ID: VersionSportStatesStateId,
        PathValues.VERSION_SPORT_PREDICTIONS_PROBABILITIES: VersionSportPredictionsProbabilities,
        PathValues.VERSION_SPORT_PREDICTIONS_PROBABILITIES_FIXTURES_FIXTURE_ID: VersionSportPredictionsProbabilitiesFixturesFixtureId,
        PathValues.VERSION_SPORT_PREDICTIONS_VALUEBETS: VersionSportPredictionsValueBets,
        PathValues.VERSION_SPORT_PREDICTIONS_VALUEBETS_FIXTURES_FIXTURE_ID: VersionSportPredictionsValueBetsFixturesFixtureId,
        PathValues.VERSION_SPORT_ODDS_PREMATCH: VersionSportOddsPreMatch,
        PathValues.VERSION_SPORT_ODDS_PREMATCH_LATEST: VersionSportOddsPreMatchLatest,
        PathValues.VERSION_SPORT_ODDS_PREMATCH_FIXTURES_FIXTURE_ID: VersionSportOddsPreMatchFixturesFixtureId,
        PathValues.VERSION_SPORT_ODDS_PREMATCH_FIXTURES_FIXTURE_ID_BOOKMAKERS_BOOKMAKER_ID: VersionSportOddsPreMatchFixturesFixtureIdBookmakersBookmakerId,
        PathValues.VERSION_SPORT_ODDS_PREMATCH_FIXTURES_FIXTURE_ID_MARKETS_MARKET_ID: VersionSportOddsPreMatchFixturesFixtureIdMarketsMarketId,
        PathValues.VERSION_SPORT_ODDS_INPLAY: VersionSportOddsInplay,
        PathValues.VERSION_SPORT_ODDS_INPLAY_LATEST: VersionSportOddsInplayLatest,
        PathValues.VERSION_SPORT_ODDS_INPLAY_FIXTURES_FIXTURE_ID: VersionSportOddsInplayFixturesFixtureId,
        PathValues.VERSION_SPORT_ODDS_INPLAY_FIXTURES_FIXTURE_ID_BOOKMAKERS_BOOKMAKER_ID: VersionSportOddsInplayFixturesFixtureIdBookmakersBookmakerId,
        PathValues.VERSION_SPORT_ODDS_INPLAY_FIXTURES_FIXTURE_ID_MARKETS_MARKET_ID: VersionSportOddsInplayFixturesFixtureIdMarketsMarketId,
        PathValues.VERSION_MY_ENRICHMENTS: VersionMyEnrichments,
        PathValues.VERSION_MY_RESOURCES: VersionMyResources,
        PathValues.VERSION_MY_LEAGUES: VersionMyLeagues,
        PathValues.VERSION_ODDS_MARKETS: VersionOddsMarkets,
        PathValues.VERSION_ODDS_MARKETS_MARKET_ID: VersionOddsMarketsMarketId,
        PathValues.VERSION_ODDS_MARKETS_SEARCH_NAME: VersionOddsMarketsSearchName,
        PathValues.VERSION_SPORT_FIXTURES_UPCOMING_MARKETS_MARKET_ID: VersionSportFixturesUpcomingMarketsMarketId,
        PathValues.VERSION_ODDS_BOOKMAKERS: VersionOddsBookmakers,
        PathValues.VERSION_ODDS_BOOKMAKERS_BOOKMAKER_ID: VersionOddsBookmakersBookmakerId,
        PathValues.VERSION_ODDS_BOOKMAKERS_SEARCH_NAME: VersionOddsBookmakersSearchName,
        PathValues.VERSION_ODDS_BOOKMAKERS_FIXTURES_FIXTURE_ID: VersionOddsBookmakersFixturesFixtureId,
        PathValues.VERSION_ODDS_BOOKMAKERS_FIXTURES_FIXTURE_ID_MAPPING: VersionOddsBookmakersFixturesFixtureIdMapping,
    }
)

path_to_api = PathToApi(
    {
        PathValues.VERSION_CORE_CONTINENTS: VersionCoreContinents,
        PathValues.VERSION_CORE_CONTINENTS_CONTINENT_ID: VersionCoreContinentsContinentId,
        PathValues.VERSION_CORE_COUNTRIES: VersionCoreCountries,
        PathValues.VERSION_CORE_COUNTRIES_COUNTRY_ID: VersionCoreCountriesCountryId,
        PathValues.VERSION_CORE_COUNTRIES_SEARCH_NAME: VersionCoreCountriesSearchName,
        PathValues.VERSION_CORE_REGIONS: VersionCoreRegions,
        PathValues.VERSION_CORE_REGIONS_REGION_ID: VersionCoreRegionsRegionId,
        PathValues.VERSION_CORE_REGIONS_SEARCH_NAME: VersionCoreRegionsSearchName,
        PathValues.VERSION_CORE_CITIES: VersionCoreCities,
        PathValues.VERSION_CORE_CITIES_CITY_ID: VersionCoreCitiesCityId,
        PathValues.VERSION_CORE_CITIES_SEARCH_NAME: VersionCoreCitiesSearchName,
        PathValues.VERSION_CORE_TYPES: VersionCoreTypes,
        PathValues.VERSION_CORE_TYPES_TYPE_ID: VersionCoreTypesTypeId,
        PathValues.VERSION_SPORT_LEAGUES: VersionSportLeagues,
        PathValues.VERSION_SPORT_LEAGUES_LIVE: VersionSportLeaguesLive,
        PathValues.VERSION_SPORT_LEAGUES_LEAGUE_ID: VersionSportLeaguesLeagueId,
        PathValues.VERSION_SPORT_LEAGUES_LEAGUE_ID_JERSEYS: VersionSportLeaguesLeagueIdJerseys,
        PathValues.VERSION_SPORT_LEAGUES_LEAGUE_ID_INCLUDES: VersionSportLeaguesLeagueIdIncludes,
        PathValues.VERSION_SPORT_LEAGUES_DATE_DATE: VersionSportLeaguesDateDate,
        PathValues.VERSION_SPORT_LEAGUES_COUNTRIES_COUNTRY_ID: VersionSportLeaguesCountriesCountryId,
        PathValues.VERSION_SPORT_LEAGUES_SEARCH_NAME: VersionSportLeaguesSearchName,
        PathValues.VERSION_SPORT_FIXTURES: VersionSportFixtures,
        PathValues.VERSION_SPORT_FIXTURES_LATEST: VersionSportFixturesLatest,
        PathValues.VERSION_SPORT_FIXTURES_FIXTURE_ID: VersionSportFixturesFixtureId,
        PathValues.VERSION_SPORT_FIXTURES_SEARCH_NAME: VersionSportFixturesSearchName,
        PathValues.VERSION_SPORT_FIXTURES_DATE_DATE: VersionSportFixturesDateDate,
        PathValues.VERSION_SPORT_FIXTURES_MULTI_FIXTURE_IDS: VersionSportFixturesMultiFixtureIds,
        PathValues.VERSION_SPORT_FIXTURES_BETWEEN_START_DATE_END_DATE: VersionSportFixturesBetweenStartDateEndDate,
        PathValues.VERSION_SPORT_FIXTURES_BETWEEN_START_DATE_END_DATE_TEAM_ID: VersionSportFixturesBetweenStartDateEndDateTeamId,
        PathValues.VERSION_SPORT_FIXTURES_HEADTOHEAD_FIRST_TEAM_SECOND_TEAM: VersionSportFixturesHeadToHeadFirstTeamSecondTeam,
        PathValues.VERSION_SPORT_LIVESCORES_LATEST: VersionSportLivescoresLatest,
        PathValues.VERSION_SPORT_LIVESCORES: VersionSportLivescores,
        PathValues.VERSION_SPORT_LIVESCORES_INPLAY: VersionSportLivescoresInplay,
        PathValues.VERSION_SPORT_TEAMS: VersionSportTeams,
        PathValues.VERSION_SPORT_TEAMS_COUNTRIES_COUNTRY_ID: VersionSportTeamsCountriesCountryId,
        PathValues.VERSION_SPORT_TEAMS_SEASONS_SEASON_ID: VersionSportTeamsSeasonsSeasonId,
        PathValues.VERSION_SPORT_TEAMS_SEARCH_NAME: VersionSportTeamsSearchName,
        PathValues.VERSION_SPORT_TEAMS_TEAM_ID: VersionSportTeamsTeamId,
        PathValues.VERSION_SPORT_TEAMS_TEAM_ID_LEAGUES: VersionSportTeamsTeamIdLeagues,
        PathValues.VERSION_SPORT_TEAMS_TEAM_ID_LEAGUES_CURRENT: VersionSportTeamsTeamIdLeaguesCurrent,
        PathValues.VERSION_SPORT_STANDINGS: VersionSportStandings,
        PathValues.VERSION_SPORT_STANDINGS_SEASONS_SEASON_ID: VersionSportStandingsSeasonsSeasonId,
        PathValues.VERSION_SPORT_STANDINGS_ROUNDS_ROUND_ID: VersionSportStandingsRoundsRoundId,
        PathValues.VERSION_SPORT_STANDINGS_CORRECTIONS_SEASONS_SEASON_ID: VersionSportStandingsCorrectionsSeasonsSeasonId,
        PathValues.VERSION_SPORT_STANDINGS_LIVE_LEAGUES_LEAGUE_ID: VersionSportStandingsLiveLeaguesLeagueId,
        PathValues.VERSION_SPORT_SCHEDULES_SEASONS_SEASON_ID: VersionSportSchedulesSeasonsSeasonId,
        PathValues.VERSION_SPORT_SCHEDULES_SEASONS_SEASON_ID_TEAMS_TEAM_ID: VersionSportSchedulesSeasonsSeasonIdTeamsTeamId,
        PathValues.VERSION_SPORT_SCHEDULES_TEAMS_TEAM_ID: VersionSportSchedulesTeamsTeamId,
        PathValues.VERSION_SPORT_PLAYERS: VersionSportPlayers,
        PathValues.VERSION_SPORT_PLAYERS_LATEST: VersionSportPlayersLatest,
        PathValues.VERSION_SPORT_PLAYERS_PLAYER_ID: VersionSportPlayersPlayerId,
        PathValues.VERSION_SPORT_PLAYERS_COUNTRIES_COUNTRY_ID: VersionSportPlayersCountriesCountryId,
        PathValues.VERSION_SPORT_PLAYERS_SEARCH_NAME: VersionSportPlayersSearchName,
        PathValues.VERSION_SPORT_NEWS_PREMATCH: VersionSportNewsPreMatch,
        PathValues.VERSION_SPORT_NEWS_PREMATCH_SEASONS_SEASON_ID: VersionSportNewsPreMatchSeasonsSeasonId,
        PathValues.VERSION_SPORT_NEWS_PREMATCH_UPCOMING: VersionSportNewsPreMatchUpcoming,
        PathValues.VERSION_SPORT_NEWS_POSTMATCH: VersionSportNewsPostMatch,
        PathValues.VERSION_SPORT_NEWS_POSTMATCH_SEASONS_SEASON_ID: VersionSportNewsPostMatchSeasonsSeasonId,
        PathValues.VERSION_SPORT_NEWS_POSTMATCH_UPCOMING: VersionSportNewsPostMatchUpcoming,
        PathValues.VERSION_SPORT_VENUES: VersionSportVenues,
        PathValues.VERSION_SPORT_VENUES_VENUE_ID: VersionSportVenuesVenueId,
        PathValues.VERSION_SPORT_VENUES_SEARCH_NAME: VersionSportVenuesSearchName,
        PathValues.VERSION_SPORT_VENUES_SEASONS_SEASON_ID: VersionSportVenuesSeasonsSeasonId,
        PathValues.VERSION_SPORT_SEASONS: VersionSportSeasons,
        PathValues.VERSION_SPORT_SEASONS_SEASON_ID: VersionSportSeasonsSeasonId,
        PathValues.VERSION_SPORT_SEASONS_TEAMS_TEAM_ID: VersionSportSeasonsTeamsTeamId,
        PathValues.VERSION_SPORT_SEASONS_SEARCH_NAME: VersionSportSeasonsSearchName,
        PathValues.VERSION_SPORT_SQUADS_TEAMS_TEAM_ID: VersionSportSquadsTeamsTeamId,
        PathValues.VERSION_SPORT_SQUADS_SEASONS_SEASON_ID_TEAMS_TEAM_ID: VersionSportSquadsSeasonsSeasonIdTeamsTeamId,
        PathValues.VERSION_SPORT_TVSTATIONS: VersionSportTvStations,
        PathValues.VERSION_SPORT_TVSTATIONS_TV_STATION_ID: VersionSportTvStationsTvStationId,
        PathValues.VERSION_SPORT_TVSTATIONS_FIXTURES_FIXTURE_ID: VersionSportTvStationsFixturesFixtureId,
        PathValues.VERSION_SPORT_COACHES: VersionSportCoaches,
        PathValues.VERSION_SPORT_COACHES_LATEST: VersionSportCoachesLatest,
        PathValues.VERSION_SPORT_COACHES_COACH_ID: VersionSportCoachesCoachId,
        PathValues.VERSION_SPORT_COACHES_COUNTRIES_COUNTRY_ID: VersionSportCoachesCountriesCountryId,
        PathValues.VERSION_SPORT_COACHES_SEARCH_NAME: VersionSportCoachesSearchName,
        PathValues.VERSION_SPORT_TOPSCORERS_STAGES_STAGE_ID: VersionSportTopscorersStagesStageId,
        PathValues.VERSION_SPORT_TOPSCORERS_SEASONS_SEASON_ID: VersionSportTopscorersSeasonsSeasonId,
        PathValues.VERSION_SPORT_ROUNDS: VersionSportRounds,
        PathValues.VERSION_SPORT_ROUNDS_ROUND_ID: VersionSportRoundsRoundId,
        PathValues.VERSION_SPORT_ROUNDS_SEARCH_NAME: VersionSportRoundsSearchName,
        PathValues.VERSION_SPORT_ROUNDS_SEASONS_SEASON_ID: VersionSportRoundsSeasonsSeasonId,
        PathValues.VERSION_SPORT_STAGES: VersionSportStages,
        PathValues.VERSION_SPORT_STAGES_STAGE_ID: VersionSportStagesStageId,
        PathValues.VERSION_SPORT_STAGES_SEARCH_NAME: VersionSportStagesSearchName,
        PathValues.VERSION_SPORT_STAGES_SEASONS_SEASON_ID: VersionSportStagesSeasonsSeasonId,
        PathValues.VERSION_SPORT_RIVALS: VersionSportRivals,
        PathValues.VERSION_SPORT_RIVALS_TEAMS_TEAM_ID: VersionSportRivalsTeamsTeamId,
        PathValues.VERSION_SPORT_COMMENTARIES: VersionSportCommentaries,
        PathValues.VERSION_SPORT_COMMENTARIES_FIXTURES_FIXTURE_ID: VersionSportCommentariesFixturesFixtureId,
        PathValues.VERSION_SPORT_REFEREES: VersionSportReferees,
        PathValues.VERSION_SPORT_REFEREES_REFEREE_ID: VersionSportRefereesRefereeId,
        PathValues.VERSION_SPORT_REFEREES_SEASONS_SEASON_ID: VersionSportRefereesSeasonsSeasonId,
        PathValues.VERSION_SPORT_REFEREES_COUNTRIES_COUNTRY_ID: VersionSportRefereesCountriesCountryId,
        PathValues.VERSION_SPORT_REFEREES_SEARCH_NAME: VersionSportRefereesSearchName,
        PathValues.VERSION_SPORT_TRANSFERS: VersionSportTransfers,
        PathValues.VERSION_SPORT_TRANSFERS_LATEST: VersionSportTransfersLatest,
        PathValues.VERSION_SPORT_TRANSFERS_TRANSFER_ID: VersionSportTransfersTransferId,
        PathValues.VERSION_SPORT_TRANSFERS_BETWEEN_START_DATE_END_DATE: VersionSportTransfersBetweenStartDateEndDate,
        PathValues.VERSION_SPORT_TRANSFERS_TEAMS_TEAM_ID: VersionSportTransfersTeamsTeamId,
        PathValues.VERSION_SPORT_TRANSFERS_PLAYERS_PLAYER_ID: VersionSportTransfersPlayersPlayerId,
        PathValues.VERSION_SPORT_STATES: VersionSportStates,
        PathValues.VERSION_SPORT_STATES_STATE_ID: VersionSportStatesStateId,
        PathValues.VERSION_SPORT_PREDICTIONS_PROBABILITIES: VersionSportPredictionsProbabilities,
        PathValues.VERSION_SPORT_PREDICTIONS_PROBABILITIES_FIXTURES_FIXTURE_ID: VersionSportPredictionsProbabilitiesFixturesFixtureId,
        PathValues.VERSION_SPORT_PREDICTIONS_VALUEBETS: VersionSportPredictionsValueBets,
        PathValues.VERSION_SPORT_PREDICTIONS_VALUEBETS_FIXTURES_FIXTURE_ID: VersionSportPredictionsValueBetsFixturesFixtureId,
        PathValues.VERSION_SPORT_ODDS_PREMATCH: VersionSportOddsPreMatch,
        PathValues.VERSION_SPORT_ODDS_PREMATCH_LATEST: VersionSportOddsPreMatchLatest,
        PathValues.VERSION_SPORT_ODDS_PREMATCH_FIXTURES_FIXTURE_ID: VersionSportOddsPreMatchFixturesFixtureId,
        PathValues.VERSION_SPORT_ODDS_PREMATCH_FIXTURES_FIXTURE_ID_BOOKMAKERS_BOOKMAKER_ID: VersionSportOddsPreMatchFixturesFixtureIdBookmakersBookmakerId,
        PathValues.VERSION_SPORT_ODDS_PREMATCH_FIXTURES_FIXTURE_ID_MARKETS_MARKET_ID: VersionSportOddsPreMatchFixturesFixtureIdMarketsMarketId,
        PathValues.VERSION_SPORT_ODDS_INPLAY: VersionSportOddsInplay,
        PathValues.VERSION_SPORT_ODDS_INPLAY_LATEST: VersionSportOddsInplayLatest,
        PathValues.VERSION_SPORT_ODDS_INPLAY_FIXTURES_FIXTURE_ID: VersionSportOddsInplayFixturesFixtureId,
        PathValues.VERSION_SPORT_ODDS_INPLAY_FIXTURES_FIXTURE_ID_BOOKMAKERS_BOOKMAKER_ID: VersionSportOddsInplayFixturesFixtureIdBookmakersBookmakerId,
        PathValues.VERSION_SPORT_ODDS_INPLAY_FIXTURES_FIXTURE_ID_MARKETS_MARKET_ID: VersionSportOddsInplayFixturesFixtureIdMarketsMarketId,
        PathValues.VERSION_MY_ENRICHMENTS: VersionMyEnrichments,
        PathValues.VERSION_MY_RESOURCES: VersionMyResources,
        PathValues.VERSION_MY_LEAGUES: VersionMyLeagues,
        PathValues.VERSION_ODDS_MARKETS: VersionOddsMarkets,
        PathValues.VERSION_ODDS_MARKETS_MARKET_ID: VersionOddsMarketsMarketId,
        PathValues.VERSION_ODDS_MARKETS_SEARCH_NAME: VersionOddsMarketsSearchName,
        PathValues.VERSION_SPORT_FIXTURES_UPCOMING_MARKETS_MARKET_ID: VersionSportFixturesUpcomingMarketsMarketId,
        PathValues.VERSION_ODDS_BOOKMAKERS: VersionOddsBookmakers,
        PathValues.VERSION_ODDS_BOOKMAKERS_BOOKMAKER_ID: VersionOddsBookmakersBookmakerId,
        PathValues.VERSION_ODDS_BOOKMAKERS_SEARCH_NAME: VersionOddsBookmakersSearchName,
        PathValues.VERSION_ODDS_BOOKMAKERS_FIXTURES_FIXTURE_ID: VersionOddsBookmakersFixturesFixtureId,
        PathValues.VERSION_ODDS_BOOKMAKERS_FIXTURES_FIXTURE_ID_MAPPING: VersionOddsBookmakersFixturesFixtureIdMapping,
    }
)
