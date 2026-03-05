def extract_player_info(soup_info, player_id):
    
    # Define variables
    player_info = {}
    list_number = 0
    
    # Adding the player id as the first value
    player_info['Player ID'] = player_id
    player_info['Last Updated'] = datetime.now()
    
    try:
        # Extracting the required information
        player_info['Image URL'] = soup_info.find('img')['src']
        player_info['Name'] = soup_info.find_all('h1')[list_number].find('span').text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return player_info, "error"
    
    try:
        player_info['Pronunciation'] = soup_info.find_all('p')[list_number].text.split(': ')[1]
        list_number +=1
    except Exception as e:
        player_info['Pronunciation'] = ""
        

    try:
        player_info['Full Name'] = soup_info.find_all('p')[list_number].text.split('\n ')[0].strip()
        
        
        try:
            player_info['Twitter'] = soup_info.find_all('p')[list_number].find_all('a', href=lambda href: href and 'twitter.com' in href)[0].text.strip()
        except:
            player_info['Twitter'] = ""         

        try:
            player_info['Instagram'] = soup_info.find_all('p')[list_number].find_all('a', href=lambda href: href and 'instagram.com' in href)[0].text.strip()
        except:
            player_info['Instagram'] = ""       
        
        list_number +=1 
        
    except Exception as e:
        player_info['Full Name'] = ""
        print(f"Error: {e}")
        return player_info, "error"

        

    try:
        # temp means an auxiliar row
        temp = soup_info.find_all('p')[list_number].find(class_='desc')
        if temp is not None:
            list_number +=1
            temp = soup_info.find_all('p')[list_number].text.strip().strip("(").strip(")").split(", ")
            player_info['Nicknames'] = str(temp)
            list_number +=1
        else:
            temp = soup_info.find_all('p')[list_number].text.strip().strip("(").strip(")").split(", ")
            if temp[0].find("Position"):
                player_info['Nicknames'] = str(temp)
                list_number +=1    
            else:
                player_info['Nicknames'] = ""

        
    except Exception as e:
        player_info['Nicknames'] = ""
        print(f"Error: {e}")
        return player_info, "error"
    

    try:
        player_info['Position'] = soup_info.find_all('p')[list_number].text.replace("\n", "").strip().split(": ")[1].split("▪")[0].strip().replace(" and ", ", ")
        player_info['Shoots'] = soup_info.find_all('p')[list_number].text.replace("\n", "").strip().split(": ")[-1].strip()
        list_number +=1
    except Exception as e:
        player_info['Position'] = ""
        player_info['Shoots'] = ""
        print(list_number)
        print(f"Exception on Position or Shoots: {e}")
        return player_info, "error"
    

    try:
        player_info['Height'] = soup_info.find_all('p')[list_number].find_all('span')[0].text.strip()
        player_info['Weight'] = soup_info.find_all('p')[list_number].find_all('span')[1].text.strip()
        list_number +=1
    except Exception as e:
        player_info['Height'] = ""
        player_info['Weight'] = ""
        print(list_number)
        print(f"Exception on Height or Weight: {e}")
        return player_info, "error"
    
    try:
        temp = soup_info.find_all('p')[list_number].text
        if temp.find("Team") >= 0:
            player_info['Team'] = soup_info.find_all('p')[list_number].text.split(": ")[1].strip()
            list_number +=1    
        else:
            player_info['Team'] = ""
    except Exception as e:
        player_info['Team'] = ""
        print(list_number)
        print(f"Exception on Team: {e}")
        return player_info, "error"
    

    try:
        player_info['Date of Birth'] = soup_info.find_all('p')[list_number].find('span', id='necro-birth')['data-birth']
        player_info['Place of Birth'] = soup_info.find_all('p')[list_number].find_all('span')[-2].text.strip().replace("\xa0", " ").replace("in ", "")
        list_number +=1
    except Exception as e:
        player_info['Date of Birth'] = ""
        player_info['Place of Birth'] = ""
        print(list_number)
        print(f"Exception on Date of Birth or Place of Birth: {e}")
        return player_info, "error"
    

        
    try:
        player_info['Relatives'] = soup_parsed.find_all('p')[list_number].text.replace("\xa0"," ").split("Relatives: ")[1].replace(" ", ": ",1)
        list_number +=1
    except Exception as e:
        player_info['Relatives'] = ""
    
            
        
        
    try:
        player_info['College'] = soup_parsed.find_all('p')[list_number].text.replace("\n", "").strip().split(": ")[1].replace("  ","").strip()
        list_number +=1
    except Exception as e:
        player_info['College'] = ""
        print(list_number)
        print(f"Exception on College: {e}")
        return player_info, "error"
    

    try:
        high_schools = soup_info.find_all('p')[list_number].text.replace("\n", "").strip().split(": ")[1].split(",   ")
        temp = [school.strip() for school in high_schools]
        player_info['High Schools'] = str(temp)
        list_number +=1
    except Exception as e:
        player_info['High Schools'] = ""
        print(list_number)
        print(f"Exception on High Schools: {e}")
        return player_info, "error"
    

    try:
        recruiting_year = int(soup_info.find_all('p')[list_number].text.replace("\n", "").split(": ")[1].strip().split(" ")[0])
        player_info['Recruiting Year'] = recruiting_year
        player_info['Recruiting Rank'] = soup_info.find_all('p')[list_number].text.replace("\n", "").split(": ")[1].strip().split(" ")[1].strip("(").strip(")")
        list_number +=1
    except Exception as e:
        player_info['Recruiting Year'] = ""
        player_info['Recruiting Rank'] = ""
    

    try:
        temp = soup_info.find_all('p')[list_number].text
        if temp.find("Draft:") >= 0:
            player_info['Draft Team'] = soup_info.find_all('p')[list_number].text.replace("\n", "").split(": ")[1].strip().split(", ")[0]
            player_info['Draft Round'] = soup_info.find_all('p')[list_number].text.replace("\n", "").split(": ")[1].strip().split(", ")[1].split(" (")[0]
            player_info['Draft Pick'] = soup_info.find_all('p')[list_number].text.replace("\n", "").split(": ")[1].strip().split(", ")[1].split(" (")[1]
            player_info['Draft Pick Overall'] = soup_info.find_all('p')[list_number].text.replace("\n", "").split(": ")[1].strip().split(", ")[2].strip(" overall)")
            player_info['Draft Year'] = soup_info.find_all('p')[list_number].text.replace("\n", "").split(": ")[1].strip().split(", ")[-1]
        else:
            player_info['Draft Team'] = ""
            player_info['Draft Round'] = ""
            player_info['Draft Pick'] = ""
            player_info['Draft Pick Overall'] = ""
            player_info['Draft Year'] = ""
        list_number +=1
    except Exception as e:
        player_info['Draft Team'] = ""
        player_info['Draft Round'] = ""
        player_info['Draft Pick'] = ""
        player_info['Draft Pick Overall'] = ""
        player_info['Draft Year'] = ""
        print(list_number)
        print(f"Exception on Draft Info: {e}")
        return player_info, "error"

    
    try:
        temp = soup_parsed.find_all('p')[list_number].text
        if temp.find("NBA Debut:") >= 0:
            player_info['NBA Debut'] = soup_parsed.find_all('p')[list_number].text.strip().split("NBA Debut: ")[1]
        list_number +=1
    except Exception as e:
        player_info['NBA Debut'] = ""
        print(f"Error: {e}")
        return player_info, "error"
    
    return player_info, ""


import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from IPython.display import clear_output

# file path
pbp_file_path = "pbp data.csv"
output_file_path = "player metadata.csv"

# Drop duplicates from final file, if any
df = pd.read_csv(pbp_file_path)
df.drop_duplicates(inplace=True)
df.reset_index(inplace=True, drop=True)

# List of columns containing player names
player_columns = [
    'shooter', 'assister', 'blocker', 'fouler', 'fouled', 'rebounder',
    'violation_player', 'free_throw_shooter', 'turnover_player',
    'turnover_causer', 'jumpball_away_player', 'jumpball_home_player',
    'jumpball_poss', 'enter_game', 'leave_game'
]

# Concatenate all player columns into a single DataFrame
list_of_players_df = pd.concat([df[col] for col in player_columns], axis=0).to_frame(name='Player')
list_of_players_df.dropna(inplace=True)
list_of_players_df.drop_duplicates(inplace=True)
list_of_players_df.reset_index(inplace=True, drop=True)

# Record the start time
start_time = time.time()

request_count = 1

players_list = []

for i, player_id in enumerate(list_of_players_df['Player']):

    if request_count % 10 == 0:
        print("Sleeping for 60 seconds")
        time.sleep(60)
        
    clear_output(wait=True)
    
    # Build URL
    current_url = f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}.html"

    # Send request and parse response
    response = requests.get(current_url)
    request_count +=1

    soup = BeautifulSoup(response.content, 'html.parser')
    soup_parsed = soup.find('div', class_='players', id='info')

    # Define list to store dictionaries
    current_dict = []
    current_dict, error_status = extract_player_info(soup_parsed, player_id)
    
    if error_status == "error":
        continue

    players_list.append(current_dict)
    
    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Iteration {i} out of {len(list_of_players_df['Player'])-1} completed. Time elapsed so far: {int(elapsed_time) // 60}min:{int(elapsed_time) & 60}s")

final_df = pd.DataFrame(players_list)
final_df.to_csv(output_file_path, index=False,header=True,mode='w')    
