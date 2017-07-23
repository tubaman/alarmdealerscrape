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

    print("waiting until ready to arm")
    client.wait_for_status("System is Ready to Arm")

    print("waiting 60 secs between status checks")
    time.sleep(60)

    print("waiting until ready to arm")
    client.wait_for_status("System is Ready to Arm")


if __name__ == '__main__':
    sys.exit(main())
