import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_basketball_players(url, url2):
    """Scrapes basketball player names and positions from the specified URL."""
    
    # Send a GET request to the webpage
    response = requests.get(url)
    response2 = requests.get(url2)
    
    # Check if the request was successful
    if response.status_code != 200 or response2.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    soup2 = BeautifulSoup(response2.content, 'html.parser')

    # Find the relevant section of the webpage
    players_data = []
    
    # Modify the following selector based on the actual HTML structure of the webpage
    player_rows = soup.select('tbody tr')  
    
    for row in player_rows:
        name = row.select_one('td[data-stat="player"] a').text.strip()  #player
        position = row.select_one('td[data-stat="pos"]').text.strip()  #position
        college = row.select_one('td[data-stat="college"]').text.strip() #college
        players_data.append({'name': name, 'position': position, 'college': college})

    print("Players without salaries:")
    for player in players_data:
        print(player)

    # Scrape salaries from the second URL
    salary_table = soup2.find('table', id='contracts')  # Assuming 'contracts' is the ID for the salary table
    if salary_table is None:
        print("Salary table not found.")
        return players_data  # Return players data even if salary table is not found

    salary_rows = salary_table.select('tbody tr')

    # Debug: Check if salary rows are found
    if not salary_rows:
        print("No salary rows found.")
    
    for row in salary_rows:
        player_th = row.select_one('th[data-stat="player"]')
        if player_th:
            name = player_th.text.strip()
            salary = row.select_one('td[data-stat="y1"]').text.strip()  # Extracting guaranteed salary

            # Debug: Check if player is found and salary is extracted
            print(f"Found salary for {name}: {salary}")

            # Update the player's data with their salary
            for player in players_data:
                if player['name'] == name:
                    player['salary(2024-2015)'] = salary
                    break

    return players_data

def save_to_json(data, filename):
    """Saves the scraped data to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)  # Writing data with an indentation for readability
    print(f"Data saved to {filename}")

def main():
    # URL of the webpage to scrape (replace with the actual URL)
    url = 'https://www.basketball-reference.com/teams/TOR/2025.html'  # Change this to the actual URL
    url2 = 'https://www.basketball-reference.com/contracts/TOR.html'
    json_directory = r'c:/Users/SJona/OneDrive/Documents/Python Scripts/scrap from website to file'  # Directory name (you can change this)
    json_filename = 'basketball_players.json'  # JSON filename
    json_path = os.path.join(json_directory, json_filename)  # Full path to save the JSON file
    
    # Create the directory if it doesn't exist
    os.makedirs(json_directory, exist_ok=True)

    players = scrape_basketball_players(url, url2)

    # Print the scraped player data
    for player in players:
        print(f"Name: {player['name']}, Position: {player['position']}, College: {player['college']}, Salary(2024-2025): {player.get('salary', 'N/A')}")
    
    if os.path.exists(json_path):
        base, extension = os.path.splitext(json_filename)
        count = 1
        
        # Generate a new filename until a unique one is found
        while os.path.exists(os.path.join(json_directory, f"{base}_{count}{extension}")):
            count += 1
        
        # Update the json_path with the new filename
        json_path = os.path.join(json_directory, f"{base}_{count}{extension}")
    # Save the data to a JSON file

    if players:
        save_to_json(players, json_path)

if __name__ == "__main__":
    main()
