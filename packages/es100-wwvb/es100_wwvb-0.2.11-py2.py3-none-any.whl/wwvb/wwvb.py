#!/usr/bin/env python3

"""

    WWVB receiver

    All times are UTC base

WWVB Location ...

    WWVB
    5701 CO-1,
    Fort Collins, CO 80524
    https://goo.gl/maps/KgRn1jDmJ3zSUfxx7

    40.678062N, 105.046688W

    https://www.nist.gov/pml/time-and-frequency-division/time-distribution/radio-station-wwvb

    North antenna coordinates: 40° 40' 51.3" N, 105° 03' 00.0" W == 40.680917 N, 105.050000 W
    South antenna coordinates: 40° 40' 28.3" N, 105° 02' 39.5" W == 40.674528 N, 105.044306 W

Speed of radio waves ...

    https://ieeexplore.ieee.org/document/1701081

    299,775 km/s in a vacuum
    299,250 km/s for 100Khz at ground level
    299,690 km/s for cm waves
    299,750 km/s for aircraft at 30,000 feet (9,800 meters)

    I choose 299,250 km/s

"""

import sys
import time
import logging
import getopt
# import configparser
from datetime import datetime, timezone, timedelta

from es100 import ES100, ES100Error, __version__
from .misc import convert_location, caculate_latency, is_it_nighttime

# ES100's pins as connected to R.Pi GPIO pins

                                        # ES100 Pin 1 == VCC 3.6V (2.0-3.6V recommended)
GPIO_IRQ  = 11 # GPIO-17                # ES100 Pin 2 == IRQ Interupt Request
                                        # ES100 Pin 3 == SCL
                                        # ES100 Pin 4 == SDA
GPIO_EN   = 7  # GPIO-4                 # ES100 Pin 5 == EN Enable
                                        # ES100 Pin 6 == GND

MY_LOCATION = [37.363056, -121.928611, 18.9]  # SJC Airport

def doit(program_name, args):
    """ doit """

    i2c_bus = None
    i2c_addr = None
    flag_debug = False
    flag_verbose = False
    es100_irq = GPIO_IRQ
    es100_en = GPIO_EN
    my_location = MY_LOCATION[:2]
    my_masl = MY_LOCATION[2]
    flag_enable_nighttime = False

    # needed within this and other modules
    required_format = '%(asctime)s %(name)s %(levelname)s %(message)s'
    logging.basicConfig(format=required_format)

    usage = program_name + ' ' + ' '.join([
                                '[-V|--version]',
                                '[-h|--help]',
                                '[-v|--verbose]',
                                '[-d|--debug]',
                                '[-b|--bus={0-999}]',
                                '[-a|--address={0-127}]',
                                '[-i|--irq={1-40}]',
                                '[-e|--en={1-40}]',
                                '[-l|--location=lat,long]',
                                '[-m|--masl=[0-99999}]',
                                '[-n|--mighttime]',
                            ])

    # config = configparser.ConfigParser()

    try:
        opts, args = getopt.getopt(args,
                                    'Vhvdb:a:i:e:l:m:n',
                                    [
                                        'version',
                                        'help',
                                        'verbose',
                                        'debug',
                                        'bus=',
                                        'address=',
                                        'size=',
                                        'irq=',
                                        'en=',
                                        'location=',
                                        'masl=',
                                        'nighttime',
                                    ])
    except getopt.GetoptError:
        sys.exit('usage: ' + usage)

    for opt, arg in opts:
        if opt in ('-V', '--version'):
            print("%s %s" % (program_name, __version__), file=sys.stderr)
            sys.exit(0)
        if opt in ('-h', '--help'):
            print("%s %s" % ('usage:', usage), file=sys.stderr)
            sys.exit(0)
        if opt in ('-v', '--verbose'):
            logging.basicConfig(level=logging.INFO)
            flag_verbose = True
            continue
        if opt in ('-d', '--debug'):
            logging.basicConfig(level=logging.DEBUG)
            flag_debug = True
            continue
        if opt in ('-b', '--bus'):
            try:
                i2c_bus = int(arg)
            except ValueError:
                print("%s %s" % (program_name, 'invalid bus'), file=sys.stderr)
                sys.exit('usage: ' + usage)
            continue
        if opt in ('-a', '--address'):
            try:
                i2c_addr = int(arg, 16)
            except ValueError:
                print("%s %s" % (program_name, 'invalid address'), file=sys.stderr)
                sys.exit('usage: ' + usage)
            continue
        if opt in ('-i', '--irq'):
            try:
                es100_irq = int(arg)
            except ValueError:
                print("%s %s" % (program_name, 'invalid irq'), file=sys.stderr)
                sys.exit('usage: ' + usage)
            continue
        if opt in ('-e', '--en'):
            try:
                es100_irq = int(arg)
            except ValueError:
                print("%s %s" % (program_name, 'invalid en'), file=sys.stderr)
                sys.exit('usage: ' + usage)
            continue
        if opt in ('-l', '--location'):
            try:
                my_location = convert_location(arg)
            except ValueError:
                print("%s %s" % (program_name, 'invalid location'), file=sys.stderr)
                sys.exit('usage: ' + usage)
            continue
        if opt in ('-m', '--masl'):
            try:
                my_masl = int(arg)
            except ValueError:
                print("%s %s" % (program_name, 'invalid masl'), file=sys.stderr)
                sys.exit('usage: ' + usage)
            continue
        if opt in ('-n', '--nighttime'):
            flag_enable_nighttime = True
            continue

    log = logging.getLogger(program_name)
    if flag_debug:
        log.setLevel(logging.DEBUG)
    if flag_verbose:
        log.setLevel(logging.INFO)

    (distance_km, bearing, latency_secs) = caculate_latency(my_location[0], my_location[1])

    log.info('The great circle distance to WWVB: %.1f Km and direction is %.1f degrees; hence latency %.3f Milliseconds',
                distance_km,
                bearing,
                latency_secs * 1000.0
            )

    latency = timedelta(microseconds=latency_secs*1000000.0)

    try:
        es100 = ES100(en=es100_en, irq=es100_irq, debug=flag_debug)
    except ES100Error as err:
        sys.exit(err)

    previous_nighttime = None
    while True:
        try:
            if flag_enable_nighttime and is_it_nighttime(my_location[0], my_location[1], my_masl):
                if previous_nighttime is not True:
                    log.info('Nighttime in-progress (Reception starting)')
                previous_nighttime = True
                received_dt = es100.time(tracking=False)
            else:
                if previous_nighttime is not False:
                    log.info('Daytime in-progress (Tracking starting)')
                previous_nighttime = False
                received_dt = es100.time(tracking=True)
        except (ES100Error, OSError) as err:
            #sys.exit(err)
            received_dt = None
            time.sleep(0.5)
        if received_dt:
            # by default WWVB has microsecond == 0 (as it's not in the receive frames)
            received_dt += latency
            now = datetime.utcnow()
            now = now.replace(tzinfo=timezone.utc)
            log.info('Time received: %s', received_dt)
            print('WWVB: %s at %s' % (received_dt, now))
            sys.stdout.flush()

def wwvb(args=None):
    """ wwvb """

    if args is None:
        args = sys.argv[1:]

    try:
        #program_name = sys.argv[0]
        program_name = 'wwvb'
        doit(program_name, args)
    except KeyboardInterrupt:
        sys.exit('^C')

    sys.exit(0)
