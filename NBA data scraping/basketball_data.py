from basketball_reference_scraper.teams import (
    get_roster, 
    get_team_stats, 
    get_opp_stats, 
    get_team_misc, 
    get_roster_stats,
    get_team_ratings
)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def fetch_team_data(team_abbreviation, season_end_year):
    """Fetches various stats for a given NBA team."""
    
    # Get the roster
    roster = get_roster(team_abbreviation, season_end_year)
    
    # Get team stats
    team_stats = get_team_stats(team_abbreviation, season_end_year, data_format='TOTALS')

    # Get opponent stats
    opp_stats = get_opp_stats(team_abbreviation, season_end_year, data_format='TOTALS')

    # Get team miscellaneous stats
    team_misc = get_team_misc(team_abbreviation, season_end_year, data_format='TOTALS')

    # Get roster stats (Player stats)
    roster_stats = get_roster_stats(team_abbreviation, season_end_year, data_format='PER_GAME')

    # Get team ratings
    team_ratings = get_team_ratings(season_end_year, team=[team_abbreviation])
    
    return roster, team_stats, opp_stats, team_misc, roster_stats, team_ratings

def visualize_data(roster, team_stats, opp_stats, team_misc, roster_stats):
    """Visualizes the basketball statistics data."""
    
    # 1. Bar chart for Points Per Game for each player
    plt.figure(figsize=(10, 6))
    sns.barplot(data=roster_stats, x='PTS', y='PLAYER', palette='viridis')
    plt.title('Points Per Game for Each Player')
    plt.xlabel('Points Per Game')
    plt.ylabel('Player')
    plt.show()
    
    # 2. Pie chart for Team Wins vs Losses
    plt.figure(figsize=(8, 8))
    labels = ['Wins', 'Losses']
    sizes = [team_misc['W'], team_misc['L']]
    colors = ['#4CAF50', '#F44336']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Team Performance: Wins vs Losses')
    plt.show()
    
    # 3. Line graph for Opponent Points Allowed
    plt.figure(figsize=(10, 6))
    plt.plot(opp_stats.index, opp_stats.values, marker='o')
    plt.title('Opponent Points Allowed Over the Season')
    plt.xlabel('Opponent Stats')
    plt.ylabel('Points Allowed')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

def main():
    # Team abbreviation and season end year
    team_abbreviation = 'GSW'  # Golden State Warriors
    season_end_year = 2024

    # Fetch the data
    roster, team_stats, opp_stats, team_misc, roster_stats, team_ratings = fetch_team_data(team_abbreviation, season_end_year)

    # Visualize the data
    visualize_data(roster, team_stats, opp_stats, team_misc, roster_stats)

if __name__ == "__main__":
    main()
