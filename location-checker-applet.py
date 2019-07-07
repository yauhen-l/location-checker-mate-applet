#!/usr/bin/env python

import threading
import time
import json
import re
from lxml import html
import requests
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('MatePanelApplet', '4.0')

from gi.repository import MatePanelApplet
from gi.repository import Gtk


def get_location():
    location = 'unknown'

    try:
        pageContent = requests.get('https://ipx.ac', timeout=1)
        tree = html.fromstring(pageContent.content)
        raw = tree.xpath('/html/body/script[9]/text()')
        match = re.match(r'.+ DATA = ({.+});.+', raw[0], re.S)

        if match:
            data = json.loads(match.group(1))
            location = data['geo']['countryName'] + ", " + data['geo']['cityName']
    except requests.exceptions.Timeout:
        location = 'timeout'
    except requests.exceptions.RequestException as e:
        print e
        location = 'exception'
    return location


class Scheduler(threading.Thread):

    def __init__(self, interval_sec, func):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interval_sec = interval_sec
        self.func = func

    def run(self):
        while True:
            self.func()
            time.sleep(self.interval_sec)


def applet_factory(applet, iid, data):
    if iid != "LocationCheckerApplet":
        return False

    # you can use this path with gio/gsettings
    settings_path = applet.get_preferences_path()

    label = Gtk.Label('')

    def update_label():
        label.set_text(get_location())

    sched = Scheduler(interval_sec=5, func=update_label)
    sched.start()

    applet.add(label)
    applet.show_all()

    return True


MatePanelApplet.Applet.factory_main("LocationCheckerAppletFactory", True,
                                    MatePanelApplet.Applet.__gtype__,
                                    applet_factory, None)
