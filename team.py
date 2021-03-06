import yaml
from datetime import datetime
from collections import deque
import calendar
import logging
import random


class Member:
    name = ''
    unavail = []
    holidays = []
    count = 0

    def __init__(self, name, unavail, holidays):
        self.name = name
        self.unavail = unavail
        self.holidays = holidays


def _read_team_from_file(teamfile):
    """ Read team information from file """
    with open(teamfile, 'r') as f:
        doc = yaml.load(f)

    return doc


def _init_team(doc):
    """ Create a list of member objects """
    members = []

    # First loop over team
    for name, data in doc['team'].items():
        logging.debug("Found member %s in file" % name )
        unavail = []
        holidays = []
        if 'unavailable' in data:
            unavail = data['unavailable']
        else:
            unavail = []
        if 'holidays' in data:
            holidays = data['holidays']
        else:
            holidays = []

        members.append(Member(name, unavail, holidays))

    random.shuffle(members)

    return members


def get_team(inputfile):
    """ Retrieve a list of member objects """
    doc = _read_team_from_file(inputfile)
    team = _init_team(doc)

    return deque(team)


def get_holidays(inputfile):
    """ Retreive a list of national holidays """
    holidays = []
    with open(inputfile, 'r') as f:
        doc = yaml.load(f)

    for day in doc['holidays']:
        holidays.append(datetime.strptime(str(day), "%Y%m%d"))

    return holidays


def check_availability(workdate, member):
    """ Determine if a member is available on a given day """
    available = None
    weekday = calendar.day_name[workdate.weekday()].lower()
    logging.debug("Checking availability for %s on date %s"
                  % (member.name, workdate))
    if member.unavail is not None:
        logging.debug("Member has unavail %s" % member.unavail)
        # Check default availability
        for k, v in member.unavail.items():
            if k == 'default':
                if weekday in v:
                    available = False
            # Check even weeks
            elif (workdate.isocalendar()[1] % 2) == 0:
                if k == 'even_week':
                    if weekday in v:
                        available = False
            # Check odd weeks
            elif (workdate.isocalendar()[1] % 2) == 1:
                if k == 'odd_week':
                    if weekday in v:
                        available = False
            # Stop if there is a match
            if available is not None:
                break

    if available is None and member.holidays is not None:
        available = _check_holidays(workdate, member)
    elif available is None:
        available = True

    return available


def _check_holidays(workdate, member):
    """ Check if member has planned holidays """
    available = True
    for day in member.holidays:
        holiday = datetime.strptime(str(day), "%Y%m%d").date()
        logging.debug("Checking for %s holiday %s with workdate %s"
                      % (member.name, holiday, workdate))
        if workdate == holiday:
            logging.debug("Member %s is not available due to holiday"
                          % member.name)
            available = False
            break

    return available
