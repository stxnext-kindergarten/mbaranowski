# -*- coding: utf-8 -*-
"""
Defines views.
"""
from calendar import day_abbr
from logging import getLogger

from flask import abort, redirect

from presence_analyzer.main import app
from presence_analyzer.utils import (
    get_data,
    group_by_weekday,
    group_by_weekday_start_end,
    jsonify,
    mean,
    mean_by_weekday,
)


log = getLogger(__name__)  # pylint: disable=invalid-name


@app.route('/')
def mainpage():
    """
    Redirects to front page.
    """
    return redirect('/static/presence_weekday.html')


@app.route('/api/v1/users', methods=['GET'])
@jsonify
def users_view():
    """
    Users listing for dropdown.
    """
    data = get_data()

    return [
        {'user_id': i, 'name': 'User {0}'.format(str(i))}
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
