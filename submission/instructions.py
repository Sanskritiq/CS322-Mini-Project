from gi.repository import Gtk
from instructions_stats import window as stat_win

class handler:

    def __init__(self, list_content, bin_content, hex_content, file_address, operations):
        self.file_address = file_address
        self.list_content = list_content
        self.bin_content = bin_content
        self.hex_content = hex_content
        self.operations = operations
        self.stat_win = None

    def on_button1_clicked(self, button):
        filename = self.file_address[:-4] + '.L'
        file_write = open(filename, 'w')
        file_write.write(self.list_content)
        file_write.close()
    def on_button2_clicked(self, button):
        filename = self.file_address[:-4] + '.bin'
        file_write = open(filename, 'w')
        file_write.write(self.bin_content)
        file_write.close()
    def on_button3_clicked(self, button):
        filename = self.file_address[:-4] + '.hex'
        file_write = open(filename, 'w')
        file_write.write(self.hex_content)
        file_write.close()
    def on_button4_clicked(self, button):
        self.stat_win = stat_win(self.operations)

# def operations_used(list_content):
#     operations = []
#     lines = list_content.split('\n')
#     for l in lines:
#         words = l.split('\t')
#         print(words)
#         operations.append(words[2])
#     return operations

class window:

    def __init__(self, list_content, bin_content, hex_content, file_address, operations):

        self.operations = operations
        print(list_content)

        self.builder = Gtk.Builder()
        self.builder.add_from_file('instructions_win.glade')
        self.builder.connect_signals(handler(list_content, bin_content, hex_content, file_address, self.operations))

        self.listing = self.builder.get_object('text1')
        self.binary = self.builder.get_object('text2')
        self.hex = self.builder.get_object('text3')

        self.listing_buffer = self.listing.get_buffer()
        self.binary_buffer = self.binary.get_buffer()
        self.hex_buffer = self.hex.get_buffer()

        self.listing_buffer.set_text(list_content)
        self.binary_buffer.set_text(bin_content)
        self.hex_buffer.set_text(hex_content)

        self.save_listing = self.builder.get_object('button1')
        self.save_bin = self.builder.get_object('button2')
        self.save_hex = self.builder.get_object('button3')

        self.instructions_stat = self.builder.get_object('button4')

        self.window = self.builder.get_object('window1')
        self.window.set_title('Instructions')

        self.window.connect('delete-event', Gtk.main_quit)
        self.window.show_all()
        Gtk.main()