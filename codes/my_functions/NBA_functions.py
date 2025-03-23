from nba_api.stats.endpoints import leaguegamefinder, teamgamelog, boxscoreadvancedv2
from nba_api.stats.static import teams, players
from nba_api.live.nba.endpoints import scoreboard

import difflib

def team_log(team_name: str):
    """
    Fetches the game log for an NBA team using its abbreviation.

    Parameters:
    -----------
    team_abbreviation : str
        The three-letter NBA team abbreviation (e.g., 'OKC' for Oklahoma City Thunder).

    Returns:
    --------
    pd.DataFrame
        A Pandas DataFrame containing the game log for the specified team.

    Raises:
    -------
    TypeError
        If the input is not a string.
    ValueError
        If the provided team abbreviation is invalid.
    
    Example:
    --------
    >>> df = team_log_by_abbrev("OKC")
    """
    if not isinstance(team_name, str):
        raise TypeError("Input must be a string representing team abbreviation(e.g., 'OKC').")
    
    team = teams.find_team_by_abbreviation(team_name)
    if team is None:
        raise ValueError(f"Invalid team abbreviation: {team_name}. Check NBA team abbreviations.")

    team_id = team['id']
    team_log = teamgamelog.TeamGameLog(team_id=team_id).get_data_frames()[0]
    return team_log


def get_team_abbreviation(team_identifier: str):
    """
    Retrieves the NBA team abbreviation for a given team identifier, regardless of case sensitivity.
    This function uses a nested dictionary of NBA teams with official names, cities, and nicknames,
    and employs difflib to handle slight misspellings in the input.

    Parameters:
        team_identifier (str): The team identifier which can be the official name, city, or nickname, in any case.

    Returns:
        str: The corresponding team abbreviation if a match is found; otherwise, returns a message indicating an unknown team or suggestion.
    """
    if not isinstance(team_identifier, str):
        raise TypeError("Input must be a string representing the team name, city, or nickname (e.g., 'OKC','thunder','Oklahoma').")
    # Nested dictionary of team data
    
    teams_dict = {
        'ATL': {'official_name': 'Atlanta Hawks', 'city': 'Atlanta', 'nicknames': ['Hawks']},
        'BOS': {'official_name': 'Boston Celtics', 'city': 'Boston', 'nicknames': ['Celtics']},
        'BKN': {'official_name': 'Brooklyn Nets', 'city': 'Brooklyn', 'nicknames': ['Nets']},
        'CHA': {'official_name': 'Charlotte Hornets', 'city': 'Charlotte', 'nicknames': ['Hornets']},
        'CHI': {'official_name': 'Chicago Bulls', 'city': 'Chicago', 'nicknames': ['Bulls']},
        'CLE': {'official_name': 'Cleveland Cavaliers', 'city': 'Cleveland', 'nicknames': ['Cavaliers', 'Cavs']},
        'DAL': {'official_name': 'Dallas Mavericks', 'city': 'Dallas', 'nicknames': ['Mavericks', 'Mavs']},
        'DEN': {'official_name': 'Denver Nuggets', 'city': 'Denver', 'nicknames': ['Nuggets']},
        'DET': {'official_name': 'Detroit Pistons', 'city': 'Detroit', 'nicknames': ['Pistons']},
        'GSW': {'official_name': 'Golden State Warriors', 'city': 'Golden State', 'nicknames': ['Warriors']},
        'HOU': {'official_name': 'Houston Rockets', 'city': 'Houston', 'nicknames': ['Rockets']},
        'IND': {'official_name': 'Indiana Pacers', 'city': 'Indiana', 'nicknames': ['Pacers']},
        'LAC': {'official_name': 'Los Angeles Clippers', 'city': 'Los Angeles', 'nicknames': ['Clippers']},
        'LAL': {'official_name': 'Los Angeles Lakers', 'city': 'Los Angeles', 'nicknames': ['Lakers']},
        'MEM': {'official_name': 'Memphis Grizzlies', 'city': 'Memphis', 'nicknames': ['Grizzlies']},
        'MIA': {'official_name': 'Miami Heat', 'city': 'Miami', 'nicknames': ['Heat']},
        'MIL': {'official_name': 'Milwaukee Bucks', 'city': 'Milwaukee', 'nicknames': ['Bucks']},
        'MIN': {'official_name': 'Minnesota Timberwolves', 'city': 'Minnesota', 'nicknames': ['Timberwolves', 'Wolves']},
        'NOP': {'official_name': 'New Orleans Pelicans', 'city': 'New Orleans', 'nicknames': ['Pelicans']},
        'NYK': {'official_name': 'New York Knicks', 'city': 'New York', 'nicknames': ['Knicks']},
        'OKC': {'official_name': 'Oklahoma City Thunder', 'city': 'Oklahoma City', 'nicknames': ['OKC Thunder','OKC', 'oklahoma city','thunder','oklahoma']},
        'ORL': {'official_name': 'Orlando Magic', 'city': 'Orlando', 'nicknames': ['Magic']},
        'PHI': {'official_name': 'Philadelphia 76ers', 'city': 'Philadelphia', 'nicknames': ['76ers', 'Sixers']},
        'PHX': {'official_name': 'Phoenix Suns', 'city': 'Phoenix', 'nicknames': ['Suns']},
        'POR': {'official_name': 'Portland Trail Blazers', 'city': 'Portland', 'nicknames': ['Trail Blazers', 'Blazers']},
        'SAC': {'official_name': 'Sacramento Kings', 'city': 'Sacramento', 'nicknames': ['Kings']},
        'SAS': {'official_name': 'San Antonio Spurs', 'city': 'San Antonio', 'nicknames': ['Spurs']},
        'TOR': {'official_name': 'Toronto Raptors', 'city': 'Toronto', 'nicknames': ['Raptors']},
        'UTA': {'official_name': 'Utah Jazz', 'city': 'Utah', 'nicknames': ['Jazz']},
        'WAS': {'official_name': 'Washington Wizards', 'city': 'Washington', 'nicknames': ['Wizards']}
    }

    # Create a lookup dictionary from teams_dict
    lookup_dict = {}
    for abbrev, info in teams_dict.items():
        lookup_dict[info['official_name'].lower()] = abbrev
        lookup_dict[info['city'].lower()] = abbrev
        for nickname in info['nicknames']:
            lookup_dict[nickname.lower()] = abbrev

    # Convert input to lowercase to match dictionary keys
    normalized_input = team_identifier.lower()

    # First, check for a direct match
    if normalized_input in lookup_dict:
        return lookup_dict[normalized_input]
    
    # If no direct match, find close matches
    close_matches = difflib.get_close_matches(normalized_input, lookup_dict.keys(), n=1, cutoff=0.8)
    if close_matches:
        return lookup_dict[close_matches[0]]
        
    return "Unknown team"


