# -*- coding: utf-8 -*-
"""
Helper functions used in views.
"""
from calendar import day_abbr
from csv import reader
from datetime import datetime
from functools import wraps
from json import dumps
from logging import getLogger

from flask import Response
from lxml import etree

from presence_analyzer.main import app


log = getLogger(__name__)  # pylint: disable=invalid-name


def jsonify(function):
    """
    Creates a response with the JSON representation of wrapped function result.
    """
    @wraps(function)
    def inner(*args, **kwargs):
        """
        This docstring will be overridden by @wraps decorator.
        """
        return Response(
            dumps(function(*args, **kwargs)),
            mimetype='application/json'
        )
    return inner


def get_data():
    """
    Extracts presence data from CSV file and groups it by user_id.

    It creates structure like this:
    data = {
        'user_id': {
            datetime.date(2013, 10, 1): {
                'start': datetime.time(9, 0, 0),
                'end': datetime.time(17, 30, 0),
            },
            datetime.date(2013, 10, 2): {
                'start': datetime.time(8, 30, 0),
                'end': datetime.time(16, 45, 0),
            },
        }
    }
    """
    data = {}

    with open(app.config['DATA_CSV'], 'r') as csvfile:
        presence_reader = reader(csvfile, delimiter=',')

        for i, row in enumerate(presence_reader):
            if len(row) != 4:
                # ignore header and footer lines
                continue

            try:
                user_id = int(row[0])
                date = datetime.strptime(row[1], '%Y-%m-%d').date()
                start = datetime.strptime(row[2], '%H:%M:%S').time()
                end = datetime.strptime(row[3], '%H:%M:%S').time()
            except (ValueError, TypeError):
                log.debug('Problem with line %d: ', i, exc_info=True)

            data.setdefault(user_id, {})[date] = {'start': start, 'end': end}

    return data


def group_by_weekday(items):
    """
    Groups presence entries by weekday.
    """
    result = {i: [] for i in range(7)}

    for date in items:
        start = items[date]['start']
        end = items[date]['end']
        result[date.weekday()].append(interval(start, end))

    return result


def seconds_since_midnight(time):
    """
    Calculates amount of seconds since midnight.
    """
    return time.hour * 3600 + time.minute * 60 + time.second


def interval(start, end):
    """
    Calculates inverval in seconds between two datetime.time objects.
    """
    return seconds_since_midnight(end) - seconds_since_midnight(start)


def mean(items):
    """
    Calculates arithmetic mean. Returns zero for empty lists.
    """
    return float(sum(items)) / len(items) if len(items) > 0 else 0


def group_by_weekday_start_end(items):
    """
    Groups the beginnings of the ends of presence entries by weekday.
    """
    result = {i: {'start': [], 'end': []} for i in range(7)}

    for date in items:
        start = seconds_since_midnight(items[date]['start'])
        end = seconds_since_midnight(items[date]['end'])
        result[date.weekday()]['start'].append(start)
        result[date.weekday()]['end'].append(end)

    return result


def mean_by_weekday(day, val):
    """
    Returns a list that contain weekday, mean of beginning and end of presence.
    """
    return [day_abbr[day], mean(val['start']), mean(val['end'])]


def get_user_data(user, url):
    """
    Returns dictionary with user's id, name, and full path to avatar.
    """
    return {
        'id': int(user.attrib['id']),
        'data': {
            'name': user.find('name').text,
            'avatar': '{}{}'.format(url, user.find('avatar').text)
        }
    }


def get_users_avatar_name():
    """
    Creates a dictionary with users' full info.

    Returns: (dict) - with user data, like:
    {
        'user_id_0': {
            'name': 'Kajetan O.',
            'avatar': 'https://intranet.stxnext.pl:443/api/images/users/130',
        },
        'user_id_1': {
            'name': 'Adam P.',
            'avatar': 'https://intranet.stxnext.pl:443/api/images/users/141',
        },
        ...
    }
    """
    all_users_data = {}
    etree_users = etree.parse(app.config['DATA_XML'])

    etree_server = etree_users.find('server')
    server_address = '{}://{}:{}'.format(
        etree_server.find('protocol').text,
        etree_server.find('host').text,
        etree_server.find('port').text
    )

    users = etree_users.find('users').xpath('//user')
    for user in users:
        user_data = get_user_data(user, server_address)
        all_users_data[user_data['id']] = user_data['data']

    return all_users_data


def get_full_users_data():
    """
    Creates a dictionary with users' full info and presence data from XML
    and CSV file and groups it by user_id.

    Returns: (dict) - with users' data, like:
    {
        'user_id': {
            'name': 'Kajetan O.',
            'avatar': '/api/images/users/130',
            'presence': {
                datetime.date(2013, 10, 1): {
                    'start': datetime.time(9, 0, 0),
                    'end': datetime.time(17, 30, 0),
                },
                datetime.date(2013, 10, 2): {
                    'start': datetime.time(8, 30, 0),
                    'end': datetime.time(16, 45, 0),
                },
            }
        },
        ...
    }
    """
    users_info = get_users_avatar_name()
    users_data = get_data()

    for user_id in users_info:
        users_info[user_id]['presence'] = users_data.setdefault(user_id, {})

    return users_info
