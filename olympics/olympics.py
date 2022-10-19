'''
    olympics.py
    Alex Widman, October 19th, 2022

    Using psycopg2 to connect to and query a PostgreSQL database (olympics).
'''
import sys
import psycopg2
import config

def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

def get_noc_gold():
    ''' List all the NOCs and the number of gold medals they have won, 
        in decreasing order of the number of gold medals. '''
    nocs = []
    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()

        # Execute the query
        query = '''SELECT teams.NOC, COUNT(event_results.outcome)
                FROM event_results, teams
                WHERE teams.id = event_results.teams_id
                AND event_results.outcome = 'Gold'
                GROUP BY teams.NOC
                ORDER BY COUNT(event_results.outcome) DESC;'''
        cursor.execute(query)

        # Iterate over the query results to produce the list of athlete names.
        for row in cursor:
            noc = row[0]
            number_gold = row[1]
            nocs.append(f'{noc} {number_gold}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return nocs

def get_athletes(search_text):
    ''' Returns a list of the full names of all the athletes
        from a specified NOC in the database.

        This function introduces an important security issue. Suppose you
        have information provided by your user (e.g. a search string)
        that needs to become part of your SQL query. Since you can't trust
        users not to be malicious, nor can you trust them not to do weird and
        accidentally destructive things, you need to be very careful about
        how you use any input they provide. To avoid the very common and
        very dangerous security attack known as "SQL Injection", we will use
        the parameterized version of cursor.execute whenever we're using
        user-generated data. See below for how that goes. '''
    athletes = []
    try:
        query = '''SELECT DISTINCT athletes.athlete_name 
                FROM athletes, teams, event_results
                WHERE athletes.id = event_results.athlete_id
                AND teams.id = event_results.teams_id
                AND teams.NOC = %s'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        index = 1
        for row in cursor:
            athlete_name = row[0]
            athletes.append(f'{athlete_name}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

def get_events(search_text):
    ''' Prints a list of all events that a specified athlete competed in. '''
    events = []
    try:
        query = '''SELECT athletes.athlete_name, events.competition_event
                FROM events, athletes, event_results
                WHERE athletes.id = event_results.athlete_id
                AND event_results.event_id = events.id
                AND athletes.athlete_name ILIKE CONCAT('%%', %s, '%%')'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        for row in cursor:
            athlete_name = row[0]
            competition_event = row[1]
            events.append(f'{athlete_name} {competition_event}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return events


def main():
    command = sys.argv[1]
    if command == '--help' or command == '--h':    
        usage = '''SYNOPSIS
      python3 olympics.py [--h] [ --help]
      python3 olmpics.py nocathletes <string>
      python3 olympics.py nocgoldmedals
      python3 olympics.py athlete_events <string>
    
    OPTIONS
    nocathletes  <string>
        List the names of all the athletes from a specified NOC.

    nocgoldmedals
        List all the NOCs and the number of gold medals they have won, 
        in decreasing order of the number of gold medals.

    eventathlete <string>
        Prints a list of all events that a specified athlete competed in.''' 
        print('')
        print(usage)
        print('')
        exit()

    elif  command == 'nocathletes': 
        if len(sys.argv) == 3:
            search_text = sys.argv[2]
            print(f'========== all the athletes from NOC "{search_text}" ==========')
            athletes = get_athletes(search_text)
            for athlete in athletes:
                print(athlete)
        else:
            print("Your command was invalid, please try again")
            exit()

    elif command == 'eventathlete':        
        if len(sys.argv) == 3:
            search_text = sys.argv[2]
            print(f'========== all events that "{search_text}" competed in ==========')
            events = get_events(search_text)
            for event in events:
                print(event)
        else:
            print("Your command was invalid, please try again")
            exit()

    elif command == 'nocgoldmedals':        
        if len(sys.argv) == 2:
            print(f'========== all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals. ==========')
            nocs = get_noc_gold()
            for noc in nocs:
                print(noc)
        else:
            print("Your command was invalid, please try again")
            exit()

    else:
        print("Your command was invalid, please try again")
        exit()

if __name__ == '__main__':
    main()