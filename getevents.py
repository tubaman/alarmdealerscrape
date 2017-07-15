#!/usr/bin/env python
import sys
import netrc
import csv

from alarmdealerscrape import AlarmDealerClient


def get_credentials():
    auth = netrc.netrc().authenticators(AlarmDealerClient.DOMAIN)
    username, account, password = auth
    return username, password


def output_as_csv(events):
    writer = csv.writer(sys.stdout)
    writer.writerow(AlarmDealerClient.EVENT_LOG_HEADERS)
    writer.writerows(events)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    username, password = get_credentials()
    client = AlarmDealerClient()
    client.login(username, password)
    events = client.get_event_log()
    output_as_csv(events)


if __name__ == '__main__':
    sys.exit(main())
