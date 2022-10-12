'''
    convert.py
    Alex Widman, October 10th, 2022
   
    # Like "Simone Arianne Biles"
    CREATE TABLE athletes (
        id INTEGER,
        name TEXT
    );
    # Like "Gymnastics Women's Individual All-Around"
    CREATE TABLE events (
        id INTEGER,
        name TEXT
    );
    # One row represents one athlete competing in one event
    # at one time.
    CREATE TABLE event_results (
        athlete_id INTEGER,
        event_id INTEGER,
        medal TEXT
    );
'''

import csv
from decimal import Rounded

# Strategy:
# (1) Create a dictionary that maps athlete IDs to athlete names
#       and then save the results in athletes.csv
# (2) Create a dictionary that maps event names to event IDs
#       and then save the results in events.csv
# (3) For each row in the original athlete_events.csv file, build a row
#       for our new event_results.csv table
#
# NOTE: I'm doing these three things in three different passes through
# the athlete_events.csv files. This is not necessary--you can do it all
# in a single pass.


# (1) Create a dictionary that maps athlete_id -> athlete_name
#       and then save the results in athletes.csv
athletes = {}
events = {}
battlegrounds = {}
teams = {}
with open('athlete_events.csv') as original_data_file,\
        open('athletes.csv', 'w') as athletes_file, open('events.csv', 'w') as events_file, open('battleground.csv', 'w') as battleground_file, open('teams.csv', 'w') as teams_file, open('event_results.csv', 'w') as event_results_file:
    reader = csv.reader(original_data_file)
    athletes_writer = csv.writer(athletes_file)
    events_writer = csv.writer(events_file)
    battleground_writer = csv.writer(battleground_file)
    teams_writer = csv.writer(teams_file)
    writer = csv.writer(event_results_file)

    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for row in reader:
        athlete_id = row[0]
        athlete_name = row[1]           #separate first and last names
        athlete_event_sex = row[2]
        if row[3] == 'NA':
            athlete_event_age = 0
        else:
            athlete_event_age = int(row[3])

        if row[4] == 'NA':
            athlete_event_height = 0
        else:
            athlete_event_height = round(float(row[4]))

        if row[5] == 'NA':
            athlete_event_weight = 0
        else:
            athlete_event_weight = round(float(row[5]))
        team_name = row[6]
        NOC_name = row[7]
        year_name = row[9]
        season_name = row[10]
        city_name = row[11]
        sport_name = row[12]
        event_name = row[13]
        sport_and_event_name = (sport_name, event_name)
        outcome = row[14]
        battleground_name = (year_name, season_name, city_name)
        team_name = (NOC_name, team_name)

        if athlete_id not in athletes:
            athletes[athlete_id] = athlete_name
            athletes_writer.writerow([athlete_id, athlete_name])    
        if sport_and_event_name not in events:       
            event_id = len(events) + 1
            events[sport_and_event_name] = event_id
            events_writer.writerow([event_id, sport_name, event_name])
        if battleground_name not in battlegrounds:    
            battleground_id = len(battlegrounds) + 1
            battlegrounds[battleground_name] = battleground_id
            battleground_writer.writerow([battleground_id, season_name, year_name, city_name])
        if team_name not in teams:       
            team_id = len(teams) + 1
            teams[team_name] = team_id
            teams_writer.writerow([team_id, team_name,  NOC_name])

        event_id = events[sport_and_event_name]
        battleground_id = battlegrounds[battleground_name]
        team_id = teams[team_name]
        writer.writerow([athlete_id, athlete_event_sex, athlete_event_age, athlete_event_height, athlete_event_weight, event_id, battleground_id, team_id, outcome])