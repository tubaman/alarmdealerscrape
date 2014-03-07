#!/usr/bin/env python
import logging
import sys
import netrc
import csv

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_credentials():
    auth = netrc.netrc().authenticators('alarmdealer.com')
    username, account, password = auth
    return username, password


def login(session, username, password):
    url = "http://alarmdealer.com/index.php?mod=auth&action=login"
    r = session.get(url)
    assert "Customer Login" in r.text
    url = "http://alarmdealer.com/index.php?mod=auth&action=authenticate"
    data = {
        'user_name': username,
        'user_pass': password,
    }
    r = session.post(url, data)
    assert "Event Log" in r.text


def get_event_log(session):
    url = "http://alarmdealer.com/index.php?mod=eventlog&action=index"
    r = session.get(url)
    soup = BeautifulSoup(r.text)
    table = soup.find('table', attrs={'class': 'listView'})
    headers = [th.text for th in table.find_all('th')]
    assert headers == ['Received', 'System', 'Signal', 'Event', 'Zone/User']
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
