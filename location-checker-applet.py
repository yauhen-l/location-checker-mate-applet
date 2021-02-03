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
gi.require_version('Notify', '0.7')

from gi.repository import Notify
from gi.repository import Gtk
from gi.repository import MatePanelApplet

appletName = 'LocationCheckerApplet'
appletFactoryName = appletName + 'Factory'


def get_location():
    location = 'unknown'

    try:
        pageContent = requests.get('https://ipx.ac', timeout=1)
        tree = html.fromstring(pageContent.content)
        raw = tree.xpath('/html/body/script[9]/text()')
        match = re.match(r'.+ DATA = ({.+});.+', raw[0], re.S)

        if match:
            data = json.loads(match.group(1))
            location = data['geo']['countryName'] + \
                ", " + data['geo']['cityName']
    except requests.exceptions.Timeout:
        location = 'timeout'
    except requests.exceptions.RequestException as e:
        print(e)
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
    if iid != appletName:
        return False

    # you can use this path with gio/gsettings
    settings_path = applet.get_preferences_path()

    initial_location = get_location()

    label = Gtk.Label(initial_location)

    # Without init libnotify crashes
    Notify.init(appletName)

    notification_title = 'Location has changed'
    n = Notify.Notification.new(notification_title, initial_location, '')

    def update_label():
        current_location = label.get_text()
        new_location = get_location()

        if new_location != current_location:
            label.set_text(new_location)
            n.update(notification_title, new_location, '')
            n.show()

    sched = Scheduler(interval_sec=5, func=update_label)
    sched.start()

    applet.add(label)
    applet.show_all()

    return True


MatePanelApplet.Applet.factory_main(appletFactoryName, True,
                                    MatePanelApplet.Applet.__gtype__,
                                    applet_factory, None)
