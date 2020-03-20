#!/usr/bin/python3

from datetime import datetime
from pyHS100 import SmartPlug
import argparse
from influxdb import InfluxDBClient
from plug_util import find_plug_ip_address, set_plug
import os
import requests
import time
import pytz


def current_value(environment):
    """
    Checks current value in the given influxdb series


    :param environment: tag to check
    :return: current value in the given series
    """
    client = InfluxDBClient(host='isengard.local', port=80, path='/influxdb',  username='root', password='root', database='garden')
    query = """select temperature from garden where time > now() - 1m and  "environment"='%s'""" % (environment)

    result = client.query(query)
    return list(result.get_points())[0]["temperature"]



def main():
    """
    Usage: run with arguments of the series and tag to check, and the ip address of the plug

    example:  >> python3 fan_equilibrium.py --environment <tag> --series <series> --plug 10.0.1.3
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dry-run", help="whether to treat this as a dry run", type=bool, default=False)
    ap.add_argument("-e", "--environment", help="influxdb tag for the series we are tracking")
    ap.add_argument("-p", "--plug-alias", help="alias of the smart plug")
    ap.add_argument("-t", "--target-temperature", help="target temperature of the environment", type=float)
    ap.add_argument("-n", "--to-numbers", help="comma separated numbers to send notifications to")
    args = vars(ap.parse_args())

    dry_run = args.get("dry_run")
    environment = args.get("environment")
    plug_alias = args.get("plug_alias")
    target_temp = args.get("target_temperature")
    plug_ip = find_plug_ip_address(plug_alias)
    print(plug_alias)
    print(plug_ip)

    current_temp = current_value(environment)
    print(current_temp)


    if (current_temp > target_temp):
        if not dry_run:
            state_changed = set_plug(plug_ip, True)
    else:
        if not dry_run:
            state_changed = set_plug(plug_ip, False)


if __name__ == "__main__":
    main()
