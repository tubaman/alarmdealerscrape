#!/usr/bin/env python
import sys
import netrc
import time

from alarmdealerscrape import AlarmDealerClient


def main(argv=None):
    if argv is None:
        argv = sys.argv

    auth = netrc.netrc().authenticators(AlarmDealerClient.DOMAIN)
    username, code, password = auth

    client = AlarmDealerClient()

    print("logging in")
    client.login(username, password)

    print("getting status")
    print(client.get_status())

    print("waiting 60 secs between status checks")
    time.sleep(60)

    print("getting status")
    print(client.get_status())

    print("waiting 120 secs between status checks")
    time.sleep(120)

    print("getting status")
    print(client.get_status())


if __name__ == '__main__':
    sys.exit(main())
