
#!/usr/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

class handler():
    def button1_clicked(self, button):
        print('halluluia')

builder = Gtk.Builder()
builder.add_from_file('test_glade.glade')
builder.connect_signals(handler())

new_button = builder.get_object('button1')
new_button.set_label('come-click-me')

new_window = builder.get_object('window1')

new_window.connect('delete-event', Gtk.main_quit)
new_window.show_all()
Gtk.main()