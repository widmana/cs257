--
--  List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation. 
-- These entities, by the way, are mostly equivalent to countries. But in some cases, you 
-- might find that a portion of a country participated in a particular games (e.g. one guy 
-- from Newfoundland in 1904) or some other oddball situation.
--
SELECT teams.NOC 
FROM teams
ORDER BY teams.NOC;


--
-- List the names of all the athletes from Jamaica. If your database design allows it, sort 
-- the athletes by last name.
--
SELECT DISTINCT athletes.athlete_name
FROM athletes, teams, event_results
WHERE athletes.id = event_results.athlete_id
AND teams.id = event_results.teams_id
AND teams.NOC = 'JAM';

--
-- List all the medals won by Greg Louganis, sorted by year. Include whatever fields in this 
-- output that you think appropriate.
-- 
SELECT event_results.outcome, battleground.competition_year, events.competition_event
FROM event_results, athletes, battleground, events
WHERE athletes.id = 71665
AND athletes.id = event_results.athlete_id
AND battleground.id = event_results.battleground_id
AND events.id = event_results.event_id
ORDER BY battleground.competition_year;

--
-- List all the NOCs and the number of gold medals they have won, in decreasing order of the 
-- number of gold medals.
-- 
SELECT teams.NOC, COUNT(event_results.outcome)
FROM event_results, teams
WHERE teams.id = event_results.teams_id
AND event_results.outcome = 'Gold'
GROUP BY teams.NOC
ORDER BY COUNT(event_results.outcome) DESC;