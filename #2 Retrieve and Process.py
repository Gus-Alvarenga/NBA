def get_pbp_table(current_url, current_game_date):
    
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get unique info from game ----------------------------------

    # Find the relevant section containing team names and scores
    score_boxes = soup.find_all('div', class_='scorebox')
    
    # Get team names
    all_a = score_boxes[0].find_all("a")
    pattern = r'\/teams\/([A-Z]{3})\/\d{4}\.html">'
    team_names = [re.findall(pattern, str(tag)) for tag in all_a]
    team_names = [item for sublist in team_names for item in sublist if item]
    away_team = team_names[0]
    home_team = team_names[1]

    # Get team scores
    all_div = score_boxes[0].find_all('div', class_='score')
    scores = [item.text for item in all_div]
    away_score = int(scores[0])
    home_score = int(scores[1])

    if away_score > home_score:
        winning_team = away_team
    else:
        winning_team = home_team

    # Get the play-by-play table ----------------------------------
    
    # Find the table element
    table = soup.find('table', {'class': 'stats_table'})

    # Iterate through the rows of the table and extract the data
    table_rows = []
    for row in table.find_all('tr'):
        cols = row.find_all(['th', 'td'])
        cols = [col.text.strip() for col in cols]
        table_rows.append(cols)

    # Find player links
    player_links = soup.find_all('a', href=True, attrs={'href': re.compile(r'^\/players\/')})
    player_dict = {}
    for link in player_links:
        player_name = link.text.strip()
        player_id = link['href'].split('/')[-1].split('.')[0]
        player_dict[player_name] = player_id

    # Replace player names with their IDs in the table
    for row in table_rows:
        for i, col in enumerate(row):
            for player_name, player_id in player_dict.items():
                col = col.replace(player_name, player_id)
            row[i] = col

    
    # Format table  ----------------------------------

    # Define a list to store the quarter information
    seconds_left_list = []
    quarter_list = []
    away_play_list = []
    away_score_increase_list = []
    away_score_list = []
    home_score_list = []
    home_score_increase_list = []
    home_play_list = []

    # Initialize start quarter
    current_quarter = 0

    # Define reference date
    reference_date = datetime(1900, 1, 1, 0, 0, 0)

    def is_valid_time(time_str):
        try:
            datetime.strptime(time_str, '%M:%S.%f')
            return True
        except ValueError:
            return False

    # Loop through the times and determine the quarter
    for i, row in enumerate(table_rows):
        if is_valid_time(row[0]) and "Start of" not in row[1] and "End of" not in row[1]:

            if i == 2 and "Jump ball:" in row[1]:

                timestamp = datetime.strptime(row[0], '%M:%S.%f')
                seconds_left = (timestamp - reference_date).total_seconds()
                seconds_left_list.append(int(seconds_left))
                quarter_list.append(current_quarter)
                away_play_list.append(row[1])
                away_score_increase_list.append("")
                away_score_list.append(0)
                home_score_list.append(0)
                home_score_increase_list.append("")
                home_play_list.append("")


            else:

                timestamp = datetime.strptime(row[0], '%M:%S.%f')
                seconds_left = (timestamp - reference_date).total_seconds()
                seconds_left_list.append(int(seconds_left))
                quarter_list.append(current_quarter)
                away_play_list.append(row[1])
                try:
                    away_score_increase_list.append(row[2])
                    away_score_list.append(int(row[3].split("-")[0]))
                    home_score_list.append(int(row[3].split("-")[1]))
                    home_score_increase_list.append(row[4])
                    home_play_list.append(row[5])

                except:
                    away_score_increase_list.append("")
                    away_score_list.append("")
                    home_score_list.append("")
                    home_score_increase_list.append("")
                    home_play_list.append("")


        elif "#q" in row[0]:
            current_quarter +=1


    # Create an empty df with specified columns
    df = pd.DataFrame(columns=['URL', 'Date', 'AwayFinalScore', 'HomeFinalScore' ,'WinningTeam', 'Quarter', 'SecondsLeft', 
                               'AwayTeam', 'AwayPlay', 'AwayScoreIncrease', 'AwayScore', 'HomeTeam', 
                               'HomePlay', 'HomeScore', 'HomeScoreIncrease'])    

    # Add table to df
    df['SecondsLeft'] = seconds_left_list
    df['Quarter'] = quarter_list
    df['AwayScore'] = away_score_list
    df['AwayPlay'] = away_play_list
    df['AwayScoreIncrease'] = away_score_increase_list
    df['HomeScoreIncrease'] = home_score_increase_list
    df['HomePlay'] = home_play_list
    df['HomeScore'] = home_score_list

    df['URL'] = current_url
    df['Date'] = current_game_date
    df['WinningTeam'] = winning_team
    df['AwayTeam'] = away_team
    df['HomeTeam'] = home_team
    df['AwayFinalScore'] = away_score
    df['HomeFinalScore'] = home_score
    
    return df

def initialize_csv():
    return {
        "shooter": "",
        "shot_type": "",
        "shot_outcome": "",
        "shot_dist": "",
        "assister": "",
        "blocker": "",
        "foul_type": "",
        "fouler": "",
        "fouled": "",
        "rebounder": "",
        "rebound_type": "",
        "stealer": "",
        "stealed": "",
        "violation_player": "",
        "violation_type": "",
        "timeout_team": "",
        "free_throw_shooter": "",
        "free_throw_outcome": "",
        "free_throw_number": "",
        "enter_game": "",
        "leave_game": "",
        "turnover_player": "",
        "turnover_type": "",
        "turnover_cause": "",
        "turnover_causer": "",
        "jumpball_away_player": "",
        "jumpball_home_player": "",
        "jumpball_poss": ""
    }

def process_line(line, csv_data):

    actions = {
        "foul": ["foul_type", "fouler", "fouled"],
        "rebound": ["rebounder", "rebound_type"],
        "steal": ["stealer","stealed"],
        "iolation": ["violation_type", "violation_player"],
        "timeout": ["timeout_team"],
        "free throw": ["free_throw_shooter", "free_throw_outcome", "free_throw_number"],
        "urnover": ["turnover_player", "turnover_type", "turnover_cause", "turnover_causer"],
        "shot": ["shooter", "shot_type", "shot_outcome", "shot_dist", "assister", "blocker"],
        "layup": ["shooter", "shot_type", "shot_outcome", "shot_dist", "assister", "blocker"],
        "dunk": ["shooter", "shot_type", "shot_outcome", "shot_dist", "assister", "blocker"],
        "enters the game": ["enter_game", "leave_game"],
        "ump ball": ["jumpball_away_player", "jumpball_home_player", "jumpball_poss"]
    }
    
    for keyword, fields in actions.items():
        if keyword in line:
            for field in fields:
                csv_data[field] = process_field(line, field)
    
    return csv_data

def process_field(line, field):
    
    if field == "foul_type":
        if "offensive foul" in line:
            return "Offensive"
        else:
            return line[:line.find(" foul")]
    if field == "fouler":
        if line.find(" (")>=0:
            return line[line.find("by ")+3:line.find(" (")]
        else: 
            return line[line.find("by ")+3:]
    if field == "fouled":
        if "drawn by " in line:
            return line[line.find("drawn by ")+9:-1]
        else:
            return ""
    if field == "rebound_type" and " rebound" in line:
        return line[:line.find(" rebound")].lower()
    if field == "rebounder":
        if line.find(" (")>=0:
            return line[line.find("by ")+3:line.find(" (")]
        else:
            return line[line.find("by ")+3:]
    if field == "stealer" and "steal" in line:
        return line[line.find("steal by ")+9:-1]
    if field == "stealed" and "steal" in line:
        return line[line.find("Turnover by ")+12:line.find(" (")]   
    if field == "violation_type" and " (" in line:
        return line[line.find("(")+1:-1]
    if field == "violation_player" and "by " in line:
        return line[line.find("by ")+3:line.find(" (")]
    if field == "timeout_team" and " full" in line:
        return line[:line.find(" full")]
    if field == "free_throw_shooter" and " " in line:
        return line[:line.find(" ")]
    if field == "free_throw_outcome":
        return "make" if "makes" in line else "miss"
    if field == "free_throw_number":
        return "technical" if "technical" in line else line[line.find("throw ")+6:]
    if field == "turnover_player" and " by " in line:
        return line[line.find(" by ")+4:line.find(" (")]
    if field == "turnover_type":
        return line[line.find("(")+1:line.find(";")] if ";" in line else line[line.find("(")+1:line.find(")")]
    if field == "turnover_cause" and "; " in line:
        return line[line.find("; ")+2:-1][:line[line.find("; ")+2:-1].find(" by")]
    if field == "turnover_causer" and "; " in line:
        return line[line.find("; ")+2:-1][line[line.find("; ")+2:-1].find(" by ")+4:]
    if field == "shooter" and "shot clock" not in line:
        return line[:line[3:].find(" ")+3]
    if field == "shot_outcome" and "shot clock" not in line:
        return "make" if "makes" in line else "miss"
    if field == "shot_type" and "shot clock" not in line:
        if "at " in line:
            value = line[line.find("makes ")+6:line.find(" at")] if "makes" in line and "at" in line else line[line.find("misses ")+7:line.find(" at")]
            return value
        return line[line.find("makes ")+6:line.find(" from")] if "makes" in line and "from" in line else line[line.find("misses ")+7:line.find(" from")]
    if field == "shot_dist" and "shot clock" not in line:
        return 0 if "at rim" in line else line[line.find("from ")+5:line.find(" ft")]
    if field == "assister" and "assist by " in line:
        return line[line.find("assist by ")+10:-1]
    if field == "blocker" and "block by " in line:
        return line[line.find("block by ")+9:-1]
    if field == "enter_game" and " enters" in line:
        return line[:line.find(" enters")]
    if field == "leave_game" and " for " in line:
        return line[line.find(" for ")+5:]
    if field == "jumpball_away_player":
        return line[line.find(": ")+2:line.find(" vs")]
    if field == "jumpball_home_player" and "vs. " in line:
        return line[line.find("vs. ")+4:line.find(" (")]
    if field == "jumpball_poss" and " gains" in line:
        return line[line.find("(")+1:line.find(" gains")]
    return ""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
from IPython.display import clear_output

# Record the start time
start_time = time.time()

# Load table of links
df_games_link_path = "nba links.csv"
df_games_link = pd.read_csv(df_games_link_path)

# Define output path
output_path = "pbp data.csv"

# Track requests and timing
request_count = 0
request_limit = 10
final_df = pd.DataFrame()
minute_start_time = datetime.now()

for i, url in enumerate(df_games_link['game_link']):
    
    # Request rate management
    request_count += 1
    if request_count == request_limit:
        elapsed = (datetime.now() - minute_start_time).total_seconds()
        if elapsed < 60:
            sleep_time = 60 - elapsed
            print(f"Rate limit hit. Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        request_count = 0
        minute_start_time = datetime.now()
    
    # Clear the console
    clear_output(wait=True)
    print(f"Iteration {i+1} out of {len(df_games_link['game_link'])}: {((i+1)/(len(df_games_link['game_link']))*100):.2f}%")

    game_date = df_games_link['game_date'][i]

    df_main = get_pbp_table(url, game_date)

    header = initialize_csv()
    df_pbp = pd.DataFrame(columns=header.keys())


    for i in range(len(df_main)):
        header = initialize_csv()
        if df_main['AwayPlay'][i]: 
            current_line = process_line(df_main['AwayPlay'][i], header)

        elif df_main['HomePlay'][i]:
            current_line = process_line(df_main['HomePlay'][i], header)


        # Concatenate the new row with df_pbp
        new_row = pd.DataFrame([current_line])
        df_pbp = pd.concat([df_pbp, new_row], ignore_index=True)
        del current_line

    # Concatenate dfs side by side
    temp_df = pd.concat([df_main, df_pbp], axis=1)

    # Concatenate all dfs
    final_df = pd.concat([final_df, temp_df], axis=0)


# Drop duplicates and export
final_df.drop_duplicates(inplace=True)
final_df.reset_index(inplace=True, drop=True)
final_df.to_csv(output_path, index=False,header=True,mode='w')

# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"\n\nTime elapsed: {int(elapsed_time)} seconds")
