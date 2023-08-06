import unittest
from .pbpstatsapi import PBPStatsClient


class TestPbpstatsRequests(unittest.TestCase):

    def setUp(self):
        self.client = PBPStatsClient()

    def test_get_game_stats(self, params={"GameId": "0022100001",
                                          "Type": "Player"}):
        response = self.client.get_game_stats(params)
        self.assertNotEqual(response, None)

    def test_get_league_players(self):
        response = self.client.get_league_players()
        self.assertNotEqual(response, None)

    def test_get_all_season_stats(self, params_list=[{
        # Lineup is a PlayerId hyphenated list. This one is the Warrior's 2022-2023 championship lineup
        "EntityType": "Lineup",
        "EntityId": "201939-202691-203084-203110-2738"
    }, {
        "EntityType": "Team",
        "EntityId": "1610612748"  # TeamId
    }, {
        "EntityType": "Player",  # Use LineupOpponent to get opponent stats
        "EntityId": "201939-202691-203084-203110-2738"
    }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_all_season_stats(params)
                self.assertNotEqual(response, None)

    def test_get_game_logs(self, params_list=[
        {
            "Season": "2021-22",  # To get for multiple seasons, separate seasons by comma
            "SeasonType": "Regular Season",
            "EntityId": "1627759-1628369-1629057-201143-203935",
            "EntityType": "Lineup"  # Use LineupOpponent to get opponent stats
        }, {
            "Season": "2021-22",  # To get for multiple seasons, separate seasons by comma
            "SeasonType": "Regular Season",
            "EntityId": "1610612737",  # ATL Hawks
            "EntityType": "Team"  # Use Opponent to get opponent stats
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_game_logs(params, total=True)
                self.assertNotEqual(response, None)

    def test_get_league_year_over_year_plots(self, params_list=[
        {
            "SeasonType": "Regular Season",
            "LeftAxis": "PtsPer100Poss",
            "RightAxis": "SecondsPerPoss"
        }, {
            "SeasonType": "Regular Season",
            "LeftAxis": "Avg3ptShotDistance",
            "RightAxis": "Avg2ptShotDistance"
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_league_year_over_year_plots(
                    params)
                self.assertNotEqual(response, None)

    def test_get_games(self, params_list=[
        {
            "Season": "2021-22",
            "SeasonType": "Regular Season"
        }, {
            "Season": "2021-22",
            "SeasonType": "Playoffs"
        }, {
            "Season": "2021-22",
            "SeasonType": "All"
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_games(
                    params)
                self.assertNotEqual(response, None)

    def test_get_lineup_opponent_summary(self, params_list=[
        {
            # lineup ids are hyphen separated player ids sorted as strings
            "LineupId": "1627759-1628369-1629057-201143-203935",
            "TeamId": "1610612738",
            "Season": "2021-22",
            "SeasonType": "Regular Season"
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_lineup_opponent_summary(
                    params)
                self.assertNotEqual(response, None)

    def test_get_lineup_player_stats(self, params_list=[
        {
            # lineup ids are hyphen separated player ids sorted as strings
            "LineupId": "1627759-1628369-1629057-201143-203935",
            "TeamId": "1610612738",
            "Season": "2021-22",
            "SeasonType": "Regular Season"
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_lineup_player_stats(
                    params)
                self.assertNotEqual(response, None)

    def test_get_lineup_subunit_stats(self, params_list=[
        {
            # lineup ids are hyphen separated player ids SORTED BY PLAYERID strings
            "LineupId": "1627759-1628369-1629057-201143-203935",
            "TeamId": "1610612738",
            "Season": "2021-22",
            "SeasonType": "Regular Season",
            "SubUnitSize": 3
        },
        {
            # lineup ids are hyphen separated player ids sorted as strings
            "LineupId": "1627759-1628369-1629057-201143-203935",
            "TeamId": "1610612738",
            "Season": "2022-23",
            "SeasonType": "Regular Season",
            "SubUnitSize": 2
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_lineup_subunit_stats(
                    params)
                self.assertNotEqual(response, None)

    def test_get_playing_time_dist(self, params={
        "TeamId": "1610612751",
        "Season": "2021-22",
        "SeasonType": "Regular Season",
        "PlayerId": "201142"
    }):
        response = self.client.get_playing_time_dist(params)
        self.assertNotEqual(response, None)

    def test_get_scatter_plots(self, params={
        "Season": "2021-22",
        "SeasonType": "Regular Season",
        "Xaxis": "PtsPer100Poss",  # see list of available stat keys below
        "Yaxis": "SecondsPerPoss",  # see list of available stat keys below
        "XaxisType": "Team",  # Team or Opponent
        "YaxisType": "Team"  # Team or Opponent
    }):
        response = self.client.get_scatter_plots(params)
        self.assertNotEqual(response, None)

    def test_get_score_margin_breakdown(self, params_list=[{
            "TeamId": "1610612744",
            "Season": "2015-16",
            "SeasonType": "Regular Season",
            "Period": "All"  # whole game
        }, {
            "TeamId": "1610612741",
            "Season": "2021-22",
            "SeasonType": "Regular Season",
            "Period": "4"  # 4th quarter
    }, {
        "TeamId": "1610612752",
        "Season": "2022-23",
        "SeasonType": "Regular Season",
        "Period": "All"  # 2nd quarter
    }]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_score_margin_breakdown(
                    params)
                self.assertNotEqual(response, None)

    def test_get_top_results(self, params_list=[
        # Fewest corner 3 makes by a team in a season
        {
            "SeasonType": "Regular Season",
            "EntityType": "Team",
            "Stat": "Corner3FGM",
            "Type": "season",
            "SortOrder": "Asc"
        },
        # Most corner 3 makes by a team in a game
        {
            "SeasonType": "Regular Season",
            "EntityType": "Team",  # Options are Team, Opponent, Player, Lineup, LineupOpponent
            "Stat": "Corner3FGM",
            "Type": "game"
        },
        # Most points per 100 posessions for a player over a season with atleast 100 points
        {
            "SeasonType": "Regular Season",
            "EntityType": "Player",  # Options are Team, Opponent, Player, Lineup, LineupOpponent
            "Stat": "PtsPer100Poss",
            "Type": "season",
            "MinCutOff": 100
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_top_results(
                    params)
                self.assertNotEqual(response, None)

    def test_get_score_time_summary(self, params={
        "Season": "2021-22",
        "SeasonType": "Regular Season",
        "Type": "Team",  # Options: Team, Lineup, Opponent, LineupOpponent
        "FromMargin": -3,
        "ToMargin": 3,
        "FromTime": 300,  # in seconds remaining in the period at the start of a possession
        "ToTime": 120,  # in seconds remaining in the period at the start of a possession
        "PeriodGte": 4  # Could also use PeriodLte or period less than or equal to or PeriodEquals for period equal to
    }):
        response = self.client.get_score_time_summary(params)
        self.assertNotEqual(response, None)

    def test_get_shot_query_summary(self, params={
        "Season": "2021-22",
        "SeasonType": "Regular Season",
        "Type": "Team",  # Options: Team, Lineup, Opponent, LineupOpponent
        "FromMargin": -3,
        "ToMargin": 3,
        "FromTime": 300,  # in seconds remaining in the period at the start of a possession
        "ToTime": 120,  # in seconds remaining in the period at the start of a possession
        "PeriodGte": 4  # Could also use PeriodLte or period less than or equal to or PeriodEquals for period equal to
    }):
        response = self.client.get_score_time_summary(params)
        self.assertNotEqual(response, None)

    def test_get_team_leverage(self, params_list=[
        {
            "Season": "2021-22",
            # options are Low, Medium, High and VeryHigh. Comma separated for multiple.
            "Leverage": "High,VeryHigh"
        },
        {
            "Season": "2022-23",
            # options are Low, Medium, High and VeryHigh. Comma separated for multiple.
            "Leverage": "Low,Medium,High,VeryHigh"
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_team_leverage(
                    params)
                self.assertNotEqual(response, None)

    def test_get_totals(self, params_list=[
        # All totals
        {
            "Season": "2021-22",
            "SeasonType": "Regular Season",
            "Type": "Player"
        },  # Across multiple seasons
        {
            "Season": "2021-22,2020-21",
            "SeasonType": "Regular Season",
            "Type": "Player"
        },  # Single team
        {
            "Season": "2021-22",
            "SeasonType": "Regular Season",
            "Type": "Player",
            "TeamId": "1610612738"
        },  # Across multiple seasons -- grouped by season
        {
            "Season": "2021-22,2020-21",
            "SeasonType": "Regular Season",
            "Type": "Team",  # Use Opponent for opponent stats
            "GroupBy": "season"
        },  # Any number of starters on vs opponent with all 5 starters on the floor
        {
            "Season": "2021-22",
            "SeasonType": "Regular Season",
            "Type": "Player",
            "StarterState": "5v5,4v5,3v5,2v5,1v5,0v5"
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_totals(
                    params)
                self.assertNotEqual(response, None)

    def test_get_combination_stats(self, params_list=[
        {
            "TeamId": "1610612755",  # Sixers
            "Season": "2021-22",
            "SeasonType": "Regular Season",
            "PlayerIds": "201935,203954",  # comma separated player ids - Harden and Embiid
            "OnlyCommonGames": "true"  # Only stats for games in which both Harden and Embiid played
        }, {
            "TeamId": "1610612743",  # Nuggets
            "Season": "2021-22",
            "SeasonType": "Regular Season",
            "PlayerIds": "203999",  # Jokic
            "Leverage": "Medium,High,VeryHigh"  # comma separated leverages
        }
    ]):
        for params in params_list:
            with self.subTest(params=params):
                response = self.client.get_combination_stats(
                    params)
                self.assertNotEqual(response, None)


class TestMakeFolderStructureMethods(unittest.TestCase):

    def setUp(self):
        pass


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()
    # suite.addTest(TestMakeDatasetMethods("test_get_game_logs"))
    # suite.addTest(TestMakeFolderStructureMethods())
    runner = unittest.TextTestRunner()
    runner.run(suite)
