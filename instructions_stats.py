from gi.repository import Gtk

class window:

    def __init__(self, operations):

        self.builder = Gtk.Builder()
        self.builder.add_from_file('stat_win.glade')

        self.count_total = self.builder.get_object('text1')
        self.count_r = self.builder.get_object('text2')
        self.count_i = self.builder.get_object('text3')
        self.count_j = self.builder.get_object('text4')
        self.count_ls = self.builder.get_object('text5')
        self.count_o = self.builder.get_object('text6')
        self.percent_r = self.builder.get_object('progress1')
        self.percent_i = self.builder.get_object('progress2')
        self.percent_j = self.builder.get_object('progress3')
        self.percent_ls = self.builder.get_object('progress4')
        self.percent_o = self.builder.get_object('progress5')
        self.operations = operations

        self.r_type = ["add", "sub", "and", "or", "xor", "nor", "slt", "sltu"]
        self.i_type = ["addi", "subi", "slti", "sltiu","andi", "ori", "xori", "lui", "sll", "srl", "sra", "beq"]
        self.j_type = ["j", "jal", "jr"]        
        self.ls_type = ["lw", "sw"]
        self.others = ["print", "exit", "nop"]

        self.total = 0
        self.r = 0
        self.i = 0
        self.j = 0
        self.ls = 0
        self.o = 0

        for op in self.operations:
            if op is not None:
                self.total += 1
                if op in self.r_type:
                    self.r += 1
                elif op in self.i_type:
                    self.i += 1
                elif op in self.j_type:
                    self.j += 1
                elif op in self.ls_type:
                    self.ls += 1
                else:
                    self.o += 1

        r_percent = (self.r/self.total)
        i_percent = (self.i/self.total)
        j_percent = (self.j/self.total)
        ls_percent = (self.ls/self.total)
        o_percent = (self.o/self.total)

        self.count_total_buffer = self.count_total.get_buffer()
        self.count_r_buffer = self.count_r.get_buffer()
        self.count_i_buffer = self.count_i.get_buffer()
        self.count_j_buffer = self.count_j.get_buffer()
        self.count_ls_buffer = self.count_ls.get_buffer()
        self.count_o_buffer = self.count_o.get_buffer()

        self.count_total_buffer.set_text(f'{self.total}')
        self.count_r_buffer.set_text(f'{self.r}')
        self.count_i_buffer.set_text(f'{self.i}')
        self.count_j_buffer.set_text(f'{self.j}')
        self.count_ls_buffer.set_text(f'{self.ls}')
        self.count_o_buffer.set_text(f'{self.o}')

        self.percent_r.set_fraction(r_percent)
        self.percent_i.set_fraction(i_percent)
        self.percent_j.set_fraction(j_percent)
        self.percent_ls.set_fraction(ls_percent)
        self.percent_o.set_fraction(o_percent)

        self.window = self.builder.get_object('window1')
        self.window.set_title('Instruction Statistics')

        self.window.connect('delete-event', Gtk.main_quit)
        self.window.show_all()
        Gtk.main()
