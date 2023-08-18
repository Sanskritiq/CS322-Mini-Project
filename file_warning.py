from gi.repository import Gtk

class window:

    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file('warning_dialogue.glade')

        self.window = self.builder.get_object('dialogue1')
        self.window.set_title('Warning!')

        self.window.connect('delete-event', Gtk.main_quit)
        self.window.show_all()
        Gtk.main()
