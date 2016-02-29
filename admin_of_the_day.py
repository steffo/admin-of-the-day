from datetime import date
from calendar import monthrange
import argparse
import team
import logging


# TODO
# - Controleer of member niet vlak achter elkaar werkt
# - Controleer of aantal dagen evenredig verdeeld is
# - Gegevens eerdere maanden meenemen


def create_schedule(team, holidays, workdate):
    logging.debug("Creating schedule for %s" % workdate)
    schedule = {}
    for i in range(1, monthrange(workdate.year, workdate.month)[1]+1):
        # Loop through days
        workday = workdate.replace(day=i)

        if workday.weekday() >= 0 and workday.weekday() < 5 \
                and workday not in holidays:
            member = get_next_member(workday, team)
            schedule[workday.day] = member.name

    return schedule


def get_next_member(workday, myteam):
    valid = False
    notvalid = []

    # Retreive next of list and reshuffle list
    while (valid is False):
        if len(myteam) < 1:
            print("No availability")
            return
        try:
            member = myteam.popleft()
        except IndexError:
            print("Got Error")
        # Check if member is available
        if not team.check_availability(workday, member):
            notvalid.append(member)
        else:
            member.count += 1
            myteam.append(member)
            valid = True

    for m in notvalid:
        myteam.appendleft(m)

    return member


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", type=int)
    parser.add_argument("-m", "--month", type=int)
    parser.add_argument("-i", "--inputfile")

    return parser.parse_args()

# PROGRAM FLOW
args = parse_arguments()

logging.basicConfig(level=logging.DEBUG)

workdate = date(args.year, args.month, 1)
holidays = team.get_holidays(args.inputfile)

# team = member.init_team(workdate)
myteam = team.get_team(args.inputfile)

schedule = create_schedule(myteam, holidays, workdate)

print("\nSchedule for %s\n" % str(workdate))
print("Assignment per team member\n")
for m in myteam:
    print("%s %d" % (m.name, m.count))

print("\n\nSchedule\n")
for day in schedule:
    print("%s %s" % (day, schedule[day]))
