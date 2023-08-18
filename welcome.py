from gi.repository import Gtk
from file_warning import window as dilg_win
from assemble import window as assem

class handler:

    def __init__(self):
        self.dialogue_win = None
        self.assemble_win = None
        self.file_address = None

    def on_button1_clicked(self, button):
        self.dialogue_win = None
        self.assemble_win = None
        if self.file_address == None:
            self.dialogue_win = dilg_win()
            print('Choose a file!')
        else:
            self.assemble_win = assem(self.file_address)
            print(self.file_address, 'click')

    def on_filechooser1_file_set(self, filechooser):
        self.file_address = filechooser.get_filename()
        print(self.file_address, 'choose')

class window:

    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file('welcome_win.glade')
        self.builder.connect_signals(handler())

        self.open_button = self.builder.get_object('button1')
        self.file_chooser = self.builder.get_object('filechooser1')

        self.window = self.builder.get_object('window1')
        self.window.set_title('Assembler-Interface')

        self.window.connect('delete-event', Gtk.main_quit)
        self.window.show_all()
        Gtk.main()

window()
