from gi.repository import Gtk
from instructions import window as inst_win
from assembler import assembler as asmblr

class handler:

    def __init__(self, file_address, editor_buffer, console_buffer, console_contents):
        self.file_address = file_address
        self.editor_buffer = editor_buffer
        self.console_buffer = console_buffer
        self.console_contents = console_contents
        self.editor_reset_content = None
        self.editor_save_content = None
        self.instructions_win = None

    def on_button1_clicked(self, button):
        self.instructions_win = None
        file_read = open(self.file_address, 'r')
        self.editor_reset_content = file_read.read()
        self.editor_buffer.set_text(self.editor_reset_content)
        file_read.close()
        self.console_contents += 'text is reset\n'
        self.console_buffer.set_text(self.console_contents)
        print('text reset')

    def on_button2_clicked(self, button):
        self.instructions_win = None
        file_write = open(self.file_address, 'w')
        self.editor_save_content = self.editor_buffer.get_text(self.editor_buffer.get_start_iter(),self.editor_buffer.get_end_iter(),True)
        file_write.write(self.editor_save_content)
        file_write.close()
        self.console_contents += 'text is saved\n'
        self.console_buffer.set_text(self.console_contents)
        print('text saved')

    def on_button3_clicked(self, button):
        asm = asmblr(self.file_address)
        asm.execution()
        self.console_contents += asm.console
        self.console_buffer.set_text(self.console_contents)
        lines = asm.listing.split('\n')
        for l in lines:
            words = l.split('\t')
            print(words)
        if(len(asm.errors))==0:
            self.instructions_win = inst_win(asm.listing, asm.bin, asm.hex, self.file_address, asm.operations)
        print('Assembled')

    def on_button4_clicked(self, button):
        self.instructions_win = None
        self.console_contents = ''
        self.console_buffer.set_text(self.console_contents)
        print('console is cleared')

class window:

    def __init__(self, file_address):

        self.builder = Gtk.Builder()
        self.builder.add_from_file('assemble_win.glade')

        self.reset_button = self.builder.get_object('button1')
        self.save_button = self.builder.get_object('button2')
        self.assemble_button = self.builder.get_object('button3')
        self.clear_console_button = self.builder.get_object('button4')

        self.editor = self.builder.get_object('text1')
        self.console = self.builder.get_object('text2')

        file_open = open(file_address,'r')
        self.editor_contents = file_open.read()
        self.editor_buffer = self.editor.get_buffer()
        self.editor_buffer.set_text(text=f'{self.editor_contents}')
        file_open.close()

        self.console_contents = f'{file_address}' + ' opened\n'
        self.console_buffer = self.console.get_buffer()
        self.console_buffer.set_text(text=f'{self.console_contents}')

        self.builder.connect_signals(handler(file_address, self.editor_buffer, self.console_buffer, self.console_contents))
        self.window = self.builder.get_object('window1')
        self.window.set_title('Assembler-Editor')

        self.window.connect('delete-event', Gtk.main_quit)
        self.window.show_all()
        Gtk.main()

# window('/home/sanskriti/CS322_mini_project/testing/add_10_numbers.asm')