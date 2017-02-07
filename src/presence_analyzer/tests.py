# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
import datetime
import json
import os.path
import unittest

from lxml import etree

# pylint: disable=unused-import
from presence_analyzer import main, views, utils


TEST_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.csv'
)

TEST_DATA_XML = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.xml'
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
        assert resp.headers['Location'].endswith('/presence_weekday')

    def test_api_users(self):
        """
        Test users listing.
        """
        resp = self.client.get('/api/v1/users')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        self.assertEqual(len(data), 2)
        self.assertDictEqual(
            data[0],
            {
                'user_id': 10,
                'name': 'Maciej Z. (10)',
            }
        )
        self.assertDictEqual(
            data[1],
            {
                'user_id': 11,
                'name': 'Maciej D. (11)',
            }
        )

    def test_mean_time_weekday_view(self):
        """
        Test mean time weekday view.
        """
        weekdays_means = [
            ['Mon', 24123.0],
            ['Tue', 16564.0],
            ['Wed', 25321.0],
            ['Thu', 22984.0],
            ['Fri', 6426.0],
            ['Sat', 0],
            ['Sun', 0],
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
            ['Mon', 0],
            ['Tue', 30047],
            ['Wed', 24465],
            ['Thu', 23705],
            ['Fri', 0],
            ['Sat', 0],
            ['Sun', 0],
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

    def test_group_by_weekday_start_end(self):
        """
        Test getting interval of mean presence time grouped by weekday
        """
        weekdays_means = [
            ['Mon', 33134.0, 57257.0],
            ['Tue', 33590.0, 50154.0],
            ['Wed', 33206.0, 58527.0],
            ['Thu', 35602.0, 58586.0],
            ['Fri', 47816.0, 54242.0],
            ['Sat', 0, 0],
            ['Sun', 0, 0],
        ]

        resp = self.client.get('/api/v1/presence_start_end/11')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertListEqual(weekdays_means, data)

    def test_users_info_view(self):
        """
        Test getting information about user.
        """
        user_info = {
            'user_id': 10,
            'user_name': 'Maciej Z. (10)',
            'avatar': 'https://intranet.stxnext.pl:443/api/images/users/10',
        }

        resp = self.client.get('/api/v1/users/10')
        data = json.loads(resp.data)

        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(data, user_info)

    def test_users_info_view_user_do_not_exist(self):
        """
        Test getting info for user's id that don't exist.
        """
        resp = self.client.get('/api/v1/users/0')

        self.assertEqual(resp.status_code, 404)


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """
    Utility functions tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        self.url = 'https://intranet.stxnext.pl:443'
        self.path = '/api/images/users/'

        main.app.config.update({
            'DATA_CSV': TEST_DATA_CSV,
            'DATA_XML': TEST_DATA_XML,
        })

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
        result = {
            0: [],
            1: [28800, 30600],
            2: [29700],
            3: [],
            4: [],
            5: [],
            6: [],
        }
        test_data = {
            datetime.date(2013, 10, 1): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 30, 0),
            },
            datetime.date(2013, 10, 8): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 0, 0),
            },
            datetime.date(2013, 10, 2): {
                'start': datetime.time(8, 30, 0),
                'end': datetime.time(16, 45, 0),
            },
        }

        grouped_by_weekday = utils.group_by_weekday(test_data)

        self.assertDictEqual(grouped_by_weekday, result)

    def test_group_by_weekday_start_end(self):
        """
        Test group_by_weekday_start_end method.
        """
        result = {
            0: {'start': [], 'end': []},
            1: {'start': [32400, 32400], 'end': [61200, 63000]},
            2: {'start': [30600], 'end': [60300]},
            3: {'start': [], 'end': []},
            4: {'start': [], 'end': []},
            5: {'start': [], 'end': []},
            6: {'start': [], 'end': []},
        }
        test_data = {
            datetime.date(2013, 10, 1): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 30, 0),
            },
            datetime.date(2013, 10, 8): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 0, 0),
            },
            datetime.date(2013, 10, 2): {
                'start': datetime.time(8, 30, 0),
                'end': datetime.time(16, 45, 0),
            },
        }

        data = utils.group_by_weekday_start_end(test_data)

        for day in range(7):
            self.assertListEqual(data[day]['start'], result[day]['start'])
            self.assertListEqual(data[day]['end'], result[day]['end'])

    def test_get_user_data(self):
        """
        Test checks if get_user_data returns correct structure and data.
        """
        test_user = {
            'id': 10,
            'data': {
                'name': 'Maciej Z.',
                'avatar': '{}{}10'.format(self.url, self.path),
            }
        }

        etree_users = etree.parse(main.app.config['DATA_XML'])
        user = etree_users.find('users').xpath('//user')[0]

        self.assertDictEqual(utils.get_user_data(user, self.url), test_user)

    def test_get_users_avatar_name(self):
        """
        Test checks if function creates correct data.
        """
        test_data = {
            10: {
                'name': 'Maciej Z.',
                'avatar': '{}{}10'.format(self.url, self.path),
            },
            11: {
                'name': 'Maciej D.',
                'avatar': '{}{}11'.format(self.url, self.path),
            },
        }

        self.assertDictEqual(utils.get_users_avatar_name(), test_data)

    def test_get_full_users_data(self):
        """
        Test checks if function creates correct data.
        """
        test_data = {
            10: {
                'presence': {
                    datetime.date(2013, 9, 10): {
                        'start': datetime.time(9, 39, 5),
                        'end': datetime.time(17, 59, 52),
                    },
                    datetime.date(2013, 9, 12): {
                        'start': datetime.time(10, 48, 46),
                        'end': datetime.time(17, 23, 51),
                    },
                    datetime.date(2013, 9, 11): {
                        'start': datetime.time(9, 19, 52),
                        'end': datetime.time(16, 7, 37),
                    }
                },
                'name': 'Maciej Z.',
                'avatar': '{}{}10'.format(self.url, self.path),
            },
            11: {
                'presence': {
                    datetime.date(2013, 9, 13): {
                        'start': datetime.time(13, 16, 56),
                        'end': datetime.time(15, 4, 2),
                    },
                    datetime.date(2013, 9, 12): {
                        'start': datetime.time(10, 18, 36),
                        'end': datetime.time(16, 41, 25),
                    },
                    datetime.date(2013, 9, 11): {
                        'start': datetime.time(9, 13, 26),
                        'end': datetime.time(16, 15, 27),
                    },
                    datetime.date(2013, 9, 10): {
                        'start': datetime.time(9, 19, 50),
                        'end': datetime.time(13, 55, 54),
                    },
                    datetime.date(2013, 9, 9): {
                        'start': datetime.time(9, 12, 14),
                        'end': datetime.time(15, 54, 17),
                    },
                    datetime.date(2013, 9, 5): {
                        'start': datetime.time(9, 28, 8),
                        'end': datetime.time(15, 51, 27),
                    }
                },
                'name': 'Maciej D.',
                'avatar': '{}{}11'.format(self.url, self.path),
            }
        }

        self.assertDictEqual(utils.get_full_users_data(), test_data)


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
