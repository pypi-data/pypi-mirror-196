import requests
import os


class PBPStatsClient(object):
    def __init__(self):
        pass

    def is_successful(self, response):
        return response.status_code == 200

    def get_player_name_from_id(self, player_id):
        """Get player name from the player id
        """
        return self.get_league_players()[player_id]

    def get_player_id_from_name(self, player_name):
        """Get player id from the player name
        """
        league_players = self.get_league_players()['players']
        for player_id in league_players:
            if player_name.lower() == league_players[player_id].lower():
                return player_id

    def get_team_name_from_id(self, team_id):
        """Get 3-letter team name from the team id
        """
        nba_teams = self.get_teams(key='id')  # current season NBA teams
        return nba_teams[team_id]

    def get_team_id_from_name(self, team_name):
        """Get the team id from the 3-letter team name
        """
        nba_teams = self.get_teams(key='name')  # current season NBA teams
        return nba_teams[team_name]

    def get_game_stats(self, params):
        """Get game stats by player/lineup
        """
        url = "https://api.pbpstats.com/get-game-stats"

        response = requests.get(url, params=params)
        if self.is_successful(response):
            response_json = response.json()
            # dictionary with home and away stats by period
            return response_json['stats']

    def get_league_players(self):
        """Dictionary mapping player id to player name for all players that are in the database for the league
        """
        url = "https://api.pbpstats.com/get-all-players-for-league/nba"
        response = requests.get(url)
        if self.is_successful(response):
            return response.json()

    def get_all_season_stats(self, params):
        """Get career stats by season for a player/team/lineup
        """
        url = "https://api.pbpstats.com/get-all-season-stats/nba"

        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()

    def get_game_logs(self, params, total=False):
        """Get game-level or total game logs for a player/team/lineup
        """
        url = "https://api.pbpstats.com/get-game-logs/nba"
        response = requests.get(url, params=params)
        response_json = response.json()
        if total:
            return response_json['single_row_table_data']
        else:
            return response_json['multi_row_table_data']

    def get_games(self, params):
        """Get all games, with basic game data (home team, away team, home team pts, away team pts, etc.), for a season and season type
        """
        url = "https://api.pbpstats.com/get-games/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()

    def get_league_year_over_year_plots(self, params):
        """Get year-over-year league averages for various stats
        """
        url = "https://api.pbpstats.com/get-league-year-over-year-plots/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()

    def get_key_options(self, method_name: str):
        """Get all supported stat keys for the given method

        Returns:
            [list]: List of valid stat names for LeftAxis or RightAxis
        """
        if 'league_year_over_year_plots' in method_name or 'get_scatter_plots' in method_name:
            stat_keys = [
                "PtsPer100Poss",  # Points Per 100 Possessions
                "SecondsPerPoss",  # Seconds Per Possession
                "FG3APct",  # 3 Point Rate
                "Fg3Pct",  # 3pt %
                "AtRimFrequency",  # At Rim Shot Frequency
                "AtRimAccuracy",  # At Rim FG%
                "AtRimPctAssisted",  # At Rim % Assisted
                "ShortMidRangeFrequency",  # Short Mid Range Shot Frequency
                "ShortMidRangeAccuracy",  # Short Mid Range FG%
                "ShortMidRangePctAssisted",  # Short Mid Range % Assisted
                "LongMidRangeFrequency",  # Long Mid Range Shot Frequency
                "LongMidRangeAccuracy",  # Long Mid Range FG%
                "LongMidRangePctAssisted",  # Long Mid % Assisted
                "Corner3Frequency",  # Corner 3 Shot Frequency
                "Corner3Accuracy",  # Corner 3 FG%
                "Corner3PctAssisted",  # Corner 3 % Assisted
                "Arc3Frequency",  # Above The Break 3 Shot Frequency
                "Arc3Accuracy",  # Above The Break 3 FG%
                "Arc3PctAssisted",  # Above The Break 3 % Assisted
                "LiveBallTurnoverPct",  # Live Ball TO%
                "EfgPct",  # eFG%
                "DefFTReboundPct",  # DReb% - Missed FTs
                "OffFTReboundPct",  # OReb% - Missed FTs
                "DefTwoPtReboundPct",  # DReb% - Missed 2s
                "OffTwoPtReboundPct",  # OReb% - Missed 2s
                "DefThreePtReboundPct",  # DReb% - Missed 3s
                "OffThreePtReboundPct",  # OReb% - Missed 3s
                "DefFGReboundPct",  # DReb% - Missed FGs
                "OffFGReboundPct",  # OReb% - Missed FGs
                "OffAtRimReboundPct",  # At Rim OReb%
                "OffShortMidRangeReboundPct",  # Short Mid-Range OReb%
                "OffLongMidRangeReboundPct",  # Long Mid-Range OReb%
                "OffArc3ReboundPct",  # Arc 3 OReb%
                "OffCorner3ReboundPct",  # Corner 3 OReb%
                "DefAtRimReboundPct",  # At Rim DReb%
                "DefShortMidRangeReboundPct",  # Short Mid-Range DReb%
                "DefLongMidRangeReboundPct",  # Long Mid-Range DReb%
                "DefArc3ReboundPct",  # Arc 3 DReb%
                "DefCorner3ReboundPct",  # Corner 3 DReb%
                "SecondChancePtsPer100PossSecondChance",  # Second Chance Efficiency
                "PenaltyPtsPer100PossPenalty",  # Penalty Efficiency
                "SecondChanceOffPossPer100Poss",  # Second Chance Possessions Per 100 Possessions
                "FirstChancePtsPer100Poss",  # First Chance Points Per 100 Possessions
                "SecondChancePtsPer100Poss",  # Second Chance Points Per 100 Possessions
                "PenaltyOffPossPer100Poss",  # Penalty Possessions Per 100 Possessions
                "Avg2ptShotDistance",  # Avg 2pt Shot Distance
                "Avg3ptShotDistance"  # Avg 3pt Shot Distance
            ]
            return stat_keys
        elif method_name.contains('get_top_results'):
            stat_keys = [
                "AtRimFGA",
                "AtRimFGM",
                "ShortMidRangeFGA",
                "ShortMidRangeFGM",
                "LongMidRangeFGA",
                "LongMidRangeFGM",
                "Corner3FGA",
                "Corner3FGM",
                "Arc3FGA",
                "Arc3FGM",
                "UnassistedAtRim",
                "AssistedAtRim",
                "UnassistedShortMidRange",
                "AssistedShortMidRange",
                "UnassistedLongMidRange",
                "AssistedLongMidRange",
                "UnassistedCorner3",
                "AssistedCorner3",
                "UnassistedArc3",
                "AssistedArc3",
                "Fg3aBlocked",
                "Fg2aBlocked",
                "LiveBallTurnovers",
                "DeadBallTurnovers",
                "Turnovers",
                "AssistedFG2M",
                "UnassistedFG2M",
                "AssistedFG3M",
                "UnassistedFG3M",
                "Putbacks",
                "FG2A",
                "FG2M",
                "FG3A",
                "FG3M",
                "AtRimAssists",
                "Corner3Assists",
                "Arc3Assists",
                "TwoPtAssists",
                "ThreePtAssists",
                "AssistPoints",
                "OffThreePtRebounds",
                "OffTwoPtRebounds",
                "FTOffRebounds",
                "DefThreePtRebounds",
                "DefTwoPtRebounds",
                "FTDefRebounds",
                "ShootingFouls",
                "FoulsDrawn",
                "TwoPtShootingFoulsDrawn",
                "ThreePtShootingFoulsDrawn",
                "NonShootingFoulsDrawn",
                "Offensive Fouls",
                "Offensive FoulsDrawn",
                "Charge Fouls",
                "Charge FoulsDrawn",
                "Blocked2s",
                "Blocked3s",
                "TotalPoss",
                "Minutes",
                "PtsPer100Poss",
                "AtRimFrequency",
                "AtRimAccuracy",
                "AtRimPctAssisted",
                "ShortMidRangeFrequency",
                "ShortMidRangeAccuracy",
                "ShortMidRangePctAssisted",
                "LongMidRangeFrequency",
                "LongMidRangeAccuracy",
                "LongMidRangePctAssisted",
                "Corner3Frequency",
                "Corner3Accuracy",
                "Corner3PctAssisted",
                "Arc3Frequency",
                "Arc3Accuracy",
                "Arc3PctAssisted",
                "EfgPct",
                "AssistPointsPer100Poss",
                "DefFTReboundPct",
                "OffFTReboundPct",
                "DefTwoPtReboundPct",
                "OffTwoPtReboundPct",
                "DefThreePtReboundPct",
                "OffThreePtReboundPct",
                "DefFGReboundPct",
                "OffFGReboundPct",
            ]
            return stat_keys
        elif method_name.contains('get_totals'):
            start_types = [
                "All",  # All
                "OffMissedFG",  # Off Any Missed FG
                "OffMissed2",  # Off Any Missed 2
                "OffMissed3",  # Off Any Missed 3
                "OffMadeFG",  # Off Any Made FG
                "OffMade2",  # Off Any Made 2
                "OffMade3",  # Off Any Made 3
                "OffAtRimMake",  # Off At Rim Make
                "OffAtRimMiss",  # Off At Rim Miss
                "OffAtRimBlock",  # Off At Rim Block
                "OffShortMidRangeMake",  # Off Short Mid-Range Make
                "OffShortMidRangeMiss",  # Off Short Mid-Range Miss
                "OffLongMidRangeMake",  # Off Long Mid-Range Make
                "OffLongMidRangeMiss",  # Off Long Mid-Range Miss
                "OffArc3Make",  # Off Arc 3 Make
                "OffArc3Miss",  # Off Arc 3 Miss
                "OffCorner3Make",  # Off Corner 3 Make
                "OffCorner3Miss",  # Off Corner 3 Miss
                "OffFTMake",  # Off FT Make
                "OffFTMiss",  # Off FT Miss
                "OffLiveBallTurnover",  # Off Steal
                "OffDeadball",  # Off Dead Ball
                "OffTimeout",  # Off Timeout
            ]
            return start_types
        else:
            # method name provided is not valid or does not accept stat keys
            return None

    def get_lineup_opponent_summary(self, params):
        """Get lineup stats vs each lineup have faced
        """
        url = "https://api.pbpstats.com/get-lineup-opponent-summary/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()

    def get_lineup_player_stats(self, params, total=False):
        """Get game-level or total player stats conditional on the specific lineup is on the floor
        """
        url = "https://api.pbpstats.com/get-lineup-player-stats/nba"
        response = requests.get(url, params=params)

        if self.is_successful(response):
            if total:
                return response.json()['single_row_table_data']
            else:
                return response.json()['multi_row_table_data']

    def get_lineup_subunit_stats(self, params):
        """Get stats for all sub units of 2, 3 or 4 players that have played out of a 5 player lineup
        """
        url = "https://api.pbpstats.com/get-lineup-subunit-stats/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()

    def get_playing_time_dist(self, params):
        """Get when a player was on the floor for each game and the scoring margin
        """
        url = "https://api.pbpstats.com/get-playing-time-distribution/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            # StartTime and EndTime are seconds into the game
            return response.json()

    def get_relative_off_def_efficiency(self, params):
        """Get team's relative offensive (ortg) and defensive eff (drtg) compared to league averages for every season
        """
        url = "https://api.pbpstats.com/get-relative-off-def-efficiency/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            # StartTime and EndTime are seconds into the game
            return response.json()['results']

    def get_scatter_plots(self, params):
        """Get stats for a team or opponent over a season
        """
        url = "https://api.pbpstats.com/get-scatter-plots/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            # Xaxis and Yaxis can be any value from the list returned by get_stat_key_options
            return response.json()['results']

    def get_teams(self, key='id'):
        """Get mapping of team ids to 3-letter team name for the current season
        """
        response = requests.get("https://api.pbpstats.com/get-teams/nba")
        if self.is_successful(response):
            teams_map = dict()
            for item in response.json()['teams']:
                team_id = item['id']
                team_name = item['text']
                if key == 'id':
                    teams_map[team_id] = team_name
                elif key == 'name':
                    teams_map[team_name] = team_id

            return teams_map

    def get_score_margin_breakdown(self, params):
        """Get percentage of possessions a team was up/down by X points
        """
        url = "https://api.pbpstats.com/get-score-margin-breakdown/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()['margins']

    def get_top_results(self, params):
        """Get top results for a EntityType (Team, Opponent, Player, Lineup, LineupOpponent) and Stat in SortOrder (Descl, Asc) over a season or specific game
        """
        url = "https://api.pbpstats.com/get-top-results/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()['results']

    def filter_top_results(self, seasons=[], names=[], include=False):
        """Get the top results including (default) or excluding the provided seasons and/or names

        Args:
            seasons (list, optional): List of seasons. Defaults to [].
            names (list, optional): List of player or team names. Defaults to [].
        """
        pass

    def get_score_time_summary(self, params):
        """Get team and lineup stats based on scoring margin and time parameters for a season
        """
        url = "https://api.pbpstats.com/get-score-time-summary/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()['results']

    def get_shot_query_summary(self, params):
        """Get shooting stats based on scoring margin and time parameters for a season
        """
        url = "https://api.pbpstats.com/get-shot-query-summary/nba"

        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()['results']

    def get_team_leverage(self, params):
        """Get team efficiency and four factors stats based on the leverage state for the regular season
        """
        url = "https://api.pbpstats.com/get-team-leverage-summary/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()['results']

    def get_team_players_for_season(self, params):
        """Get all the players (dict mapping player id to player name) for a team (team id) for a season
        """
        url = "https://api.pbpstats.com/get-team-players-for-season"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()['players']

    def get_totals(self, params, league=False):
        """Get player/team/lineup totals for various query parameters
        """
        url = "https://api.pbpstats.com/get-totals/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            response_json = response.json()
            if league:
                return response_json["single_row_table_data"]
            else:
                return response_json["multi_row_table_data"]

    def get_combination_stats(self, params):
        """Get efficiency for all on/off combinations of players (player id) on a team (team id)
        """
        url = "https://api.pbpstats.com/get-wowy-combination-stats/nba"
        response = requests.get(url, params=params)
        if self.is_successful(response):
            return response.json()['results']

    def get_live_game_stats(self, game_id, result_type='players'):
        """Get live game stats as they happen. Issues with play-by-play data may be ammended later on.
        """
        url = f"https://api.pbpstats.com/live/game/{game_id}/{result_type}"
        response = requests.get(url)
        if self.is_successful(response):
            return response.json()

    def get_live_game_home_team(self, game_id, result_type='players'):
        headers_json = self.get_live_game_stats(
            game_id, result_type)['headers']
        home_team_full_name = headers_json[1]['label']
        return home_team_full_name

    def get_live_game_visitor_team(self, game_id, result_type='players'):
        headers_json = self.get_live_game_stats(
            game_id, result_type)['headers']
        visitor_team_full_name = headers_json[2]['label']
        return visitor_team_full_name

    def get_live_game_time(self, game_id, result_type='players'):
        return self.get_live_game_stats(game_id, result_type)['status']

    def get_live_game_stat(self, game_id, stat, result_type='players'):
        stat_rows = self.get_live_game_stats(game_id, result_type)[
            'game_data']['rows']
        for row in stat_rows:
            if row['stat'].lower() == stat.lower():
                return row

    def get_games_today(self):
        url = "https://api.pbpstats.com/live/games/nba"
        response = requests.get(url)
        if self.is_successful(response):
            return response.json()['game_data']

    def get_lineup_id_from_lineup(self, lineup: str):
        """Get lineup (sorted hyphenated list of str player id's) from list of player names
        """

        lineup_id_list = []
        lineup_name_list = lineup.split(", ")
        for name in lineup_name_list:
            player_id = self.get_player_id_from_name(name)
            lineup_id_list.append(player_id)
        lineup_id_list = sorted(lineup_id_list)
        return '-'.join(lineup_id_list)
