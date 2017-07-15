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

    print("arming")
    client.arm_stay()

    print("waiting until exit delay")
    client.wait_for_status("Exit Delay in Progress")

    print("waiting 5 secs")
    time.sleep(5)

    print("disarming")
    client.disarm(code)

    print("waiting until ready to arm")
    client.wait_for_status("System is Ready to Arm")


if __name__ == '__main__':
    sys.exit(main())
