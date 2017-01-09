# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
import datetime
import json
import os.path
import unittest

# pylint: disable=unused-import
from presence_analyzer import main, views, utils


TEST_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.csv'
)


# pylint: disable=maybe-no-member, too-many-public-methods
class PresenceAnalyzerViewsTestCase(unittest.TestCase):
    """
    Views tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})
        self.client = main.app.test_client()

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_mainpage(self):
        """
        Test main page redirect.
        """
        resp = self.client.get('/')

        self.assertEqual(resp.status_code, 302)
        assert resp.headers['Location'].endswith('/presence_weekday.html')

    def test_api_users(self):
        """
        Test users listing.
        """
        resp = self.client.get('/api/v1/users')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        self.assertEqual(len(data), 2)
        self.assertDictEqual(data[0], {u'user_id': 10, u'name': u'User 10'})

    def test_mean_time_weekday_view(self):
        """
        Test mean time weekday view.
        """
        weekdays_means = [
            ['Mon', 19733.666666666668],
            ['Tue', 19733.666666666668],
            ['Wed', 19733.666666666668],
            ['Thu', 19733.666666666668],
            ['Fri', 19733.666666666668],
            ['Sat', 19733.666666666668],
            ['Sun', 19733.666666666668],
        ]

        resp = self.client.get('/api/v1/mean_time_weekday/11')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(weekdays_means, data)

    def test_mean_time_weekday_view_user_do_not_exist(self):
        """
        Test getting weekly mean time for user's id that don't exist.
        """
        resp = self.client.get('/api/v1/mean_time_weekday/0')

        self.assertEqual(resp.status_code, 404)

    def test_presence_weekday_view(self):
        """
        Test presence weekday view.
        """
        weekdays_presence = [
            ['Weekday', 'Presence (s)'],
            ['Mon', 78217],
            ['Tue', 78217],
            ['Wed', 78217],
            ['Thu', 78217],
            ['Fri', 78217],
            ['Sat', 78217],
            ['Sun', 78217],
        ]

        resp = self.client.get('/api/v1/presence_weekday/10')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(weekdays_presence, data)

    def test_presence_weekday_view_user_do_not_exist(self):
        """
        Test getting weekly presence for user's id that don't exist.
        """
        resp = self.client.get('/api/v1/presence_weekday/0')

        self.assertEqual(resp.status_code, 404)


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """
    Utility functions tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_get_data(self):
        """
        Test parsing of CSV file.
        """
        sample_date = datetime.date(2013, 9, 10)

        data = utils.get_data()

        self.assertIsInstance(data, dict)
        self.assertItemsEqual(data.keys(), [10, 11])
        self.assertIn(sample_date, data[10])
        self.assertItemsEqual(data[10][sample_date].keys(), ['start', 'end'])
        self.assertEqual(
            data[10][sample_date]['start'],
            datetime.time(9, 39, 5)
        )

    def test_seconds_since_midnight(self):
        """
        Test seconds_since_midnight method.
        """
        time = datetime.time(1, 7, 5)

        self.assertEqual(utils.seconds_since_midnight(time), 4025)

    def test_interval(self):
        """
        Test interval method.
        """
        start = datetime.time(2, 1, 5)
        end = datetime.time(2, 5, 12)

        self.assertEqual(utils.interval(start, end), 247)

    def test_mean(self):
        """
        Test mean method.
        """
        elements = (1, 2, 3, 4, 5, 6, 7, 8, 9)

        self.assertEqual(utils.mean(elements), 5.0)
        self.assertEqual(utils.mean([]), 0)

    def test_group_by_weekday(self):
        """
        Test group_be_weekday method.
        """
        result = 7 * [[28800, 29700, 30600]]
        test_data = {
            datetime.date(2013, 10, 1): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 30, 0)
            },
            datetime.date(2013, 10, 8): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 0, 0)
            },
            datetime.date(2013, 10, 2): {
                'start': datetime.time(8, 30, 0),
                'end': datetime.time(16, 45, 0)
            },
        }

        grouped_by_weekday = utils.group_by_weekday(test_data)

        self.assertListEqual(grouped_by_weekday, result)


def suite():
    """
    Default test suite.
    """
    base_suite = unittest.TestSuite()
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    return base_suite


if __name__ == '__main__':
    unittest.main()
