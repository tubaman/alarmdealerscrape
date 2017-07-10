# alarmdealerscrape

Scrape info from [http://alarmdealer.com](http://alarmdealer.com)

## Setup

   1. `mkvirtualenv alarmdealerscrape`
   2. `pip install -r requirements.txt`
   3. Put your alarmdealer.com username and password in `~/.netrc` like this:

    machine alarmdealer.com login myusername account mycode password mypassword

## Get Alarm Events

`python getevents.py`

## Test Arm/Disarm

`python test_arm_disarm.py`
