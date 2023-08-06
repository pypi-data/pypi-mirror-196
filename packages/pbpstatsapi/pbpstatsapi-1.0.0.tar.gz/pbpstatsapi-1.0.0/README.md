# pbp-stats-client
Python client library for the example usage of the PBP Stats API

The official client for the PBP Stats API has it's documentation page [here](https://pbpstats.readthedocs.io/en/latest/). This client is meant to be used in addition to, not in place of, the official client.

# Motivation

The official PBP stats client offers 3 objects to interact with:

-Games 
-Season
-Day

And providing settings keys such as `Boxscore`, and `Possesions` allow you to access detailed data 
on the game, team, player, and lineup level.

Thus, these objects are great for collecting data, but the ease of collecting some generic and less specific data that is independent of game, season, or day was not easily available. For instance, you may be interest in getting a list of current team ids and team  names for all teams in the NBA or maybe all player_ids in the history of the NBA. This client provides easy access to this data by wrapping direct requests URL to fetch them. 

## Getting Started

You can install the package using

```
pip install pbpstatsapi
```

