#!/usr/bin/env python3

"""

Description ...

    WWVB 60Khz Full funcionality receiver/parser for i2c bus based ES100-MOD

    A time and date decoder for the ES100-MOD WWVB receiver 

Copyright ...

    Copyright (C) 2023 @mahtin - Martin J Levy - W6LHI/G8LHI - https://github.com/mahtin

Further reading ...

    See README.md

"""

import sys
import time
import logging
import getopt
# import configparser
from datetime import timedelta

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
    flag_force_tracking = False

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
                                '[-n|--nighttime]',
                                '[-t|--tracking]',
                            ])

    # config = configparser.ConfigParser()

    try:
        opts, args = getopt.getopt(args,
                                    'Vhvdb:a:i:e:l:m:nt',
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
                                        'tracking',
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
        if opt in ('-t', '--tracking'):
            flag_force_tracking = True
            continue

    log = logging.getLogger(program_name)
    if flag_debug:
        log.setLevel(logging.DEBUG)
    if flag_verbose:
        log.setLevel(logging.INFO)

    (distance_km, bearing, latency_secs) = caculate_latency(my_location[0], my_location[1])

    log.info('The great circle distance to WWVB: %.1f Km and ' +
                    'direction is %.1f degrees; ' +
                    'hence latency %.3f Milliseconds',
                distance_km,
                bearing,
                latency_secs * 1000.0
            )

    my_latency = timedelta(microseconds=latency_secs*1000000.0)

    try:
        es100 = ES100(en=es100_en, irq=es100_irq, debug=flag_debug, verbose=flag_verbose)
    except ES100Error as err:
        sys.exit(err)

    # All set. Let's start receiving till the end of time

    while True:
        received_dt = receive(es100, log, flag_force_tracking, flag_enable_nighttime, my_location, my_masl)
        if not received_dt:
            time.sleep(0.5)
            continue

        # by default WWVB has microsecond == 0 (as it's not in the receive frames)

        # Remember that my_latency we caculated based on our location?
        # We now add it into the time received time to correct for our location
        received_dt += my_latency

        sys_received_dt = es100.system_time()
        if received_dt.year == 1 and received_dt.month == 1 and received_dt.day == 1:
            # tracking result with only seconnd and microsecond being accurate
            log.info('Time received (seconds only): %02d.%03d at %s',
                        received_dt.second,
                        int(received_dt.microsecond / 1000),
                        sys_received_dt
                    )
            print('WWVB: (tracking) %02d.%03d at %s' % (
                        received_dt.second,
                        int(received_dt.microsecond / 1000),
                        sys_received_dt
                    ))
        else:
            log.info('Time received: %s', received_dt)
            print('WWVB: %s at %s' % (received_dt, sys_received_dt))
        sys.stdout.flush()

    # not reached

previous_nighttime = None

def receive(es100, log, flag_force_tracking, flag_enable_nighttime, my_location, my_masl):
    """ receive """
    global previous_nighttime

    if flag_force_tracking:
        # Always do tracking (ignore nightime flag)
        new_tracking_flag = True
        log.info('Reception starting (tracking forced on)')
    else:
        if flag_enable_nighttime:
            if  is_it_nighttime(my_location[0], my_location[1], my_masl):
                # nightime
                new_tracking_flag = False
                if previous_nighttime is not True:
                    log.info('Nighttime in-progress (Reception starting)')
                previous_nighttime = True
            else:
                # daytime
                new_tracking_flag = True
                if previous_nighttime is not False:
                    log.info('Daytime in-progress (Tracking starting)')
                previous_nighttime = False
        else:
            # Don't care about nighttime/daytime; always receive
            new_tracking_flag = False
            log.info('Reception starting')

    try:
        received_dt = es100.time(tracking=new_tracking_flag)
    except (ES100Error, OSError):
        return None

    return received_dt

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
