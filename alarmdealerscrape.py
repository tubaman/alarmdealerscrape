#!/usr/bin/env python
import logging
import sys
import netrc
import csv
from urlparse import urlunsplit
from urllib import urlencode

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


DOMAIN = 'alarmdealer.com'

EVENT_LOG_HEADERS = [
    'Received', 'System', 'Signal', 'SIA Code', 'Partition', 'Extra',
    'Zone/User', 'Relay Status'
]


def get_credentials():
    auth = netrc.netrc().authenticators(DOMAIN)
    username, account, password = auth
    return username, password


def get_url(mod, action):
    """Generate a URL given the query params

    ex:
    >>> get_url('auth', 'login')
    'https://alarmdealer.com/index.php?action=login&mod=auth'

    """
    query = urlencode({'mod': mod, 'action': action})
    parts = ('https', DOMAIN, 'index.php', query, '')
    url = urlunsplit(parts)
    return url


def login(session, username, password):
    url = get_url('auth', 'login')
    r = session.get(url)
    assert "Customer Login" in r.text
    url = get_url('auth', 'authenticate')
    data = {
        'user_name': username,
        'user_pass': password,
    }
    r = session.post(url, data)
    assert "Event Log" in r.text


def get_event_log(session):
    url = get_url('eventlog', 'index')
    r = session.get(url)
    soup = BeautifulSoup(r.text)
    table = soup.find('table', attrs={'class': 'listView'})
    headers = [th.text for th in table.find_all('th')]
    assert headers == EVENT_LOG_HEADERS, "headers(%s) have changed" % headers
    trs = table.find_all('tr')
    events = []
    for tr in trs[1:]:
        tds = tr.find_all('td')
        values = [td.text.strip() for td in tds]
        assert len(values) == len(headers)
        events.append(values)
    return events


def output_as_csv(events):
    writer = csv.writer(sys.stdout)
    writer.writerow(EVENT_LOG_HEADERS)
    writer.writerows(events)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    username, password = get_credentials()
    session = requests.Session()
    login(session, username, password)
    events = get_event_log(session)
    output_as_csv(events)


if __name__ == '__main__':
    sys.exit(main())
