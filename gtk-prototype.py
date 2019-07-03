#!/bin/python

from gi.repository import Gtk
import gi
import threading
import time
import datetime


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


gi.require_version('Gtk', '3.0')

label = Gtk.Label("Hello")
# label.set_selectable(True)


def hello():
    #t = threading.Timer(1, hello, [counter+1])
    #t.daemon = True
    # t.start()
    label.set_text("Date: %s" % datetime.datetime.now())


sched = Scheduler(interval_sec=2, func=hello)
sched.start()

win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)
win.add(label)
win.show_all()

Gtk.main()
