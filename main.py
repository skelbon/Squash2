#!/bin/bash

import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
import time
import pywhatkit

whatsapp_group_id = {
    'Moss_Side_Squash_Everyone': 'KYrbT0hC4XEC4d04YbVzrX',
    'test_group': 'JzGIx7rBAwa8AxHGwmaRlU'
}

team_URLs = {
    'Moss Side 1': 'https://nwcounties.leaguemaster.co.uk/cgi-county/icounty.exe/showteamfixtures?teamid=468&team'
                   '=Moss%20Side%201',
    'Moss Side 2': 'https://nwcounties.leaguemaster.co.uk/cgi-county/icounty.exe/showteamfixtures?teamid=469&team'
                   '=Moss%20Side%202'
}


# This function will return the date of the next day_to_get_date_of after
# todays_date. The function can be used to find the date of any weekday from
# an arbitrary date but here we're using it to find the thursday following today.

def get_date_next_thursday(todays_date, day_to_get_date_of):
    date_next_x = todays_date + datetime.timedelta(days=(day_to_get_date_of - todays_date.weekday() - 1) % 7 + 1)
    return date_next_x


def get_match_fixture(team_url, dt):
    # Function takes team name (exactly as found in Leaguemaster) and
    # returns a list with venue (home or away) and opponents
    # if there is no match on the date passed to the function it will return -1

    venue_and_opponent = []

    # Fetch the LeagueMaster website HTML
    source = requests.get(team_url).text

    # Soupify
    soup = BeautifulSoup(source, 'lxml')

    # Locate and collect all fixtures data
    all_tables = soup.find_all('table')
    content_table = all_tables[2]
    all_cells = content_table.find_all(class_='boxmain')

    # Convert data to list of strings
    texted = []
    for cell in all_cells:
        texted.append(cell.text)

    # Locate date cell for date requested if date is nt found return -1
    for i, cell in enumerate(texted):
        if dt in cell:
            index = i
            # Venue (Home or Away) are in the following 2 cells
            venue_and_opponent.append(texted[index + 1])
            venue_and_opponent.append(texted[index + 2])
            return venue_and_opponent

    no_match = 'no match'
    return no_match


# returns a line of text (team fixture) for insertion into message body
def construct_message_line(this_team):

    this_teams_fixtures_url = team_URLs[this_team]
    date_next_thursday = get_date_next_thursday(date.today(), 3)
    this_date = date_next_thursday.strftime('%d/%m/%y')
    fixture_list = get_match_fixture(this_teams_fixtures_url, this_date)

    if 'Away' in fixture_list[0]:
        message_line = this_team + ' away vs ' + fixture_list[1]
        return message_line
    elif 'Home' in fixture_list[0]:
        message_line = this_team + ' at home vs ' + fixture_list[1]
        return message_line
    else:
        message_line = this_team + ' has no match next week.'
        return message_line


whatsapp_message = 'Onward and upwards!\n\n' \
                   + 'The league games for next Thursday ' \
                   + get_date_next_thursday(date.today(), 3).strftime('%d/%m/%y') + ' are:\n\n' \
                   + construct_message_line('Moss Side 1') + '\n' \
                   + construct_message_line('Moss Side 2') + '\n\n' + 'Who\'s available?'

pywhatkit.sendwhatmsg_to_group(whatsapp_group_id['Moss_Side_Squash_Everyone'], whatsapp_message, int(time.strftime('%H')), int(time.strftime('%M')) + 2, 35, True, 12)
