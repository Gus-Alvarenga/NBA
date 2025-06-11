# NBA

This repository walks through the process of transforming text-based play-by-play data into dashboards filled with NBA player and team stats.

**TL;DR:** Basketball Reference provides play-by-play data like the image below. This project transforms that data into NBA stats and displays them in Power BI dashboards.

### Raw Data
![Basketball Reference](https://github.com/gustavo-alvarenga/About-me/blob/main/NBA%20Raw%20Data.png)

### Final Result (Click to view the interactive [dashboard](https://app.powerbi.com/view?r=eyJrIjoiZWVmYzRkYjAtMTU3OS00YTNhLWEzYTctMjA5M2U5OTE1NDU0IiwidCI6ImE2ZThmZmUwLTg1ZWYtNDBhMS1iMDU1LTUxNmU2YjY1ODJmMiJ9))
![Twitch](https://github.com/Gus-Alvarenga/About-me/blob/main/nba%20dashboard.png)

### Tools & Tech Used:
* Python
* Power BI

## Step #1: Retrieve List of Links

First, we need to retrieve the list of links. This [code](https://github.com/gustavo-alvarenga/NBA/blob/main/%231%20List%20of%20Links.py) starts from the initial set date (i.e., the first day of the season) and collects all relevant links from that point on.

It's important to mention that we don’t want to send too many requests and risk exceeding their limits. Basketball Reference (as of the time of writing) allows 10 requests per minute. You can check this information [here](https://www.sports-reference.com/bot-traffic.html).

All files will be saved locally for convenience.

## Step #2: Retrieve and Process Data

Now that we have the links, we're going to retrieve the play-by-play data and process it. Here's the [code](https://github.com/Gus-Alvarenga/NBA/blob/main/%232%20Retrieve%20and%20Process.py).

## Step #3: Players Metadata

To add a cherry on top, let’s also retrieve player metadata. You'll extract the unique players listed in the play-by-play data and gather additional info on them. Here's the [code](https://github.com/Gus-Alvarenga/NBA/blob/main/%233%20Players%20Metadata.py).

## Step #4: Visualization

Now that all the data has been retrieved, there’s a lot that can be done.

In this visualization, the focus is on player performance, including overall stats, free throw accuracy (broken down by attempt number), performance against different opponents, and scoring by distance from the arc. You can take this further and include team analysis, matchup breakdowns, and more.

Here's the [dashboard](https://app.powerbi.com/view?r=eyJrIjoiZWVmYzRkYjAtMTU3OS00YTNhLWEzYTctMjA5M2U5OTE1NDU0IiwidCI6ImE2ZThmZmUwLTg1ZWYtNDBhMS1iMDU1LTUxNmU2YjY1ODJmMiJ9)  
![Twitch](https://github.com/Gus-Alvarenga/About-me/blob/main/nba%20dashboard.png)


You can reach out to me on [LinkedIn](https://www.linkedin.com/in/gustavo-alvarenga/)
