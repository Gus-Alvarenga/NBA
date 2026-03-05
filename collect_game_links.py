from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define initial date you want to start looking for links
date_string = '2024-10-22'

# Define variables
game_list = []
not_found_count = 0
request_count = 0

while True:
    
    # Convert the date string to a datetime object
    date = datetime.strptime(date_string, '%Y-%m-%d')

    # Extract day, month, and year
    day = date.day
    month = date.month
    year = date.year
    
    # Navigate to the page
    page_html = "https://www.basketball-reference.com/boxscores/?month="+str(month)+"&day="+str(day)+"&year="+str(year)

    # Send a GET request to the URL
    response = requests.get(page_html)
    
    request_count += 1

    # Clause to respect their allowed limit!
    if request_count > 10:
        print("Pausing for 60 seconds to avoid rate limiting...")
        time.sleep(60) 
        request_count = 0

    if response.status_code == 200:

        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all 'a' elements with href that starts with '/boxscores/pbp/'
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/boxscores/pbp/')]

        # Get full link
        if links:
            complete_links = ['https://www.basketball-reference.com' + link for link in links]

            for link in complete_links:
                game_list.append({
                    'game_date': date_string,
                    'game_link': link
                })
                
            print(f"{date_string} successfully completed")
    
        else:
            not_found_count +=1
            print(f"{date_string} skipped - no games found")
            
        # Skip to next day
        delta = timedelta(days=1)
        new_date = date + delta
        date_string = new_date.strftime('%Y-%m-%d')

    else:
        print(f"Error: Failed to retrieve the page. Status code: {response.status_code}")
        # Sleep for 5 seconds and try again
        time.sleep(5)
        
    # If the number of errors exceeds 20, it's safe to say the season is over
    if not_found_count > 20:
        print(f"Season {season} is over!")
        break

# Export data to a local csv
df = pd.DataFrame(game_list)
df.to_csv('list_of_links.csv', header=True, index=False, mode='w')
