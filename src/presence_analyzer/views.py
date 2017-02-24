# -*- coding: utf-8 -*-
"""
Defines views.
"""
from calendar import day_abbr, month_name
from logging import getLogger

from flask import abort, redirect
from flask_mako import render_template
from mako.exceptions import TopLevelLookupException

from presence_analyzer.main import app
from presence_analyzer.utils import (
    get_data,
    get_full_users_data,
    get_year_month_location,
    group_by_weekday,
    group_by_weekday_start_end,
    jsonify,
    mean,
    mean_by_weekday,
)


log = getLogger(__name__)  # pylint: disable=invalid-name


@app.route('/')
def index():
    """
    Redirects to the front page.
    """
    return redirect('/templates/presence_weekday')


@app.route('/templates/<string:tab>')
def mainpage(tab):
    """
    Renders the front page.
    """
    try:
        return render_template('{}.html'.format(tab))
    except TopLevelLookupException:
        abort(404)


@app.route('/api/v1/users', methods=['GET'])
@jsonify
def users_view():
    """
    Users listing for dropdown.
    """
    data = get_full_users_data()

    return [
        {
            'user_id': i,
            'name': data[i]['name'].encode('utf-8')
        }
        for i in data.keys()
    ]


@app.route('/api/v1/mean_time_weekday/<int:user_id>', methods=['GET'])
@jsonify
def mean_time_weekday_view(user_id):
    """
    Returns mean presence time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])

    return [
        (day_abbr[weekday], mean(intervals))
        for weekday, intervals in weekdays.items()
    ]


@app.route('/api/v1/presence_weekday/<int:user_id>', methods=['GET'])
@jsonify
def presence_weekday_view(user_id):
    """
    Returns total presence time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = group_by_weekday(data[user_id])
    result = [
        (day_abbr[weekday], sum(intervals))
        for weekday, intervals in weekdays.items()
    ]
    result.insert(0, ('Weekday', 'Presence (s)'))

    return result


@app.route('/api/v1/presence_start_end/<int:user_id>', methods=['GET'])
@jsonify
def start_end_view(user_id):
    """
    Returns interval of mean presence time of given user grouped by weekday.
    """
    data = get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays_data = group_by_weekday_start_end(data[user_id])

    return [
        mean_by_weekday(weekday, intervals)
        for weekday, intervals in weekdays_data.items()
    ]


@app.route('/api/v1/users/<int:usr_id>', methods=['GET'])
@jsonify
def users_info_view(usr_id):
    """
    Returns information about given user.
    """
    data = get_full_users_data()
    if usr_id not in data:
        log.debug('User %s not found!', usr_id)
        abort(404)

    return {
        'user_id': usr_id,
        'user_name': '{} ({})'.format(
            data[usr_id]['name'].encode('utf-8'),
            usr_id
        ),
        'avatar': data[usr_id]['avatar'],
    }


@app.route('/api/v1/presence_location_view', methods=['GET'])
@jsonify
def year_month_view():
    """
    Year & month listing for a dropdown.
    """
    data = get_year_month_location()

    return [
        {
            'key': item,
            'val': '{} {}'.format(item[:4], month_name[int(item[5: 7])]),
        }
        for item in data.keys()
    ]


@app.route('/api/v1/presence_location_view/<string:date_id>', methods=['GET'])
@jsonify
def location_view(date_id):
    """
    Returns: (dict) - with location data for a given month, like:
    {
        'user_id': '2012-01',
        'locations': {
            'Pila': 3028793,
            'Poznan': 2987470,
            'Lodz': 2823194
        },
    }
    """
    data = get_year_month_location()

    if date_id not in data:
        log.debug('Data %s not found!', date_id)
        abort(404)

    return {
        'user_id': date_id,
        'locations': data[date_id],
    }
