import unittest
import team
from datetime import date


class TeamTest(unittest.TestCase):
    testfile = 'config_test.yaml'
    workdate = date(2016, 1, 25)

    def test_read_team_from_file(self):

        doc = team._read_team_from_file(self.testfile)

        self.assertIsNotNone(doc['team'])
        self.assertIsNotNone(doc['team']['alice'])
        self.assertIsNotNone(doc['team']['bob'])
        self.assertIsNotNone(doc['team']['chris'])
        self.assertIsNotNone(doc['team']['debby'])
        self.assertIsNotNone(doc['holidays'])
        self.assertIsNotNone(doc['holidays'])

    def test_init_team(self):

        doc = team._read_team_from_file(self.testfile)
        result = team._init_team(doc)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5)

        for member in result:
            if member.name == 'alice':
                self.assertEqual(len(member.unavail['default']), 2)
                self.assertIsNotNone(member.holidays)
            if member.name == 'bob':
                self.assertEqual(len(member.unavail['odd_week']), 2)
                self.assertIsNotNone(member.holidays)

    def test_get_holidays(self):

        holidays = team.get_holidays(self.testfile)
        self.assertIsNotNone(holidays)
        self.assertEqual(len(holidays), 2)

    def test_check_availability(self):
        t = team.get_team(self.testfile)

        for member in t:
            if member.name == 'alice':
                result = team.check_availability(self.workdate, member)
                self.assertFalse(result)
            elif member.name == 'bob':
                result = team.check_availability(self.workdate, member)
                self.assertFalse(result)
            elif member.name == 'chris':
                result = team.check_availability(self.workdate, member)
                self.assertTrue(result)
            elif member.name == 'debby':
                result = team.check_availability(self.workdate, member)
                self.assertTrue(result)
            elif member.name == 'dude':
                result = team.check_availability(self.workdate, member)
                self.assertFalse(result)
