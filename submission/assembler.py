import re
import math
import sys
import string


class assembler:


	def __init__(self, file_address):
		self.file_address = file_address
		self.register_mapper = ['0', 'at', 'v0', 'v1', 'a0', 'a1', 'a2', 'a3', 't0',
			't1', 't2', 't3', 't4', 't5', 't6', 't7', 's0', 's1', 's2', 's3', 's4', 's5', 's6',
			's7', 't8', 't9', 'k0', 'k1', 'gp', 'sp', 'fp', 'ra']

		self.reserved_reg = ['at', 'k0', 'k1']
		self.constant_reg = ['0']

		self.opcode_mapper = {"addi":"001001", "subi":"001000", "slti":"001010", "sltiu":"001011",
			"andi":"001100", "ori":"001101", "xori":"001110", "lui":"001111", "lw":"100011",
			"sw":"101011", "j":"000010", "jal":"000011", "jr":"000001", "beq":"000100", "print":
			"010000", "exit":"010111", "nop":"111111", "sll":"000000", "srl":"000000", "sra":"000000", 
			"add":"000000", "sub":"000000", "and":"000000", "or":"000000", "xor":"000000", "nor":"000000", "slt":"000000", "sltu":"000000"}

		self.funct_mapper = {"sll":"000000", "srl":"000010", "sra":"000011", "add":"100000",
			"sub":"100010", "and":"100100", "or":"100101", "xor":"100110", "nor":"100111",
			"slt":"101010", "sltu":"101011"}

		self.r_shft = ["sll", "srl", "sra"]
		self.r_rest = ["add", "sub", "and", "or", "xor", "nor", "slt", "sltu"]
		self.i_type = ["addi", "subi", "slti", "sltiu","andi", "ori", "xori", "lui"]
		self.j_type = ["j", "jal", "jr", "beq"]
		self.ls_type = ["lw", "sw"]
		self.others = ["print", "exit", "nop"]

		self.no_arg = ["exit", "nop"]
		self.one_arg = ["j", "jal", "jr", "print"]	
		self.two_arg =  ["lw", "sw"]
		self.three_arg = ["beq"] + ["add", "sub", "and", "or", "xor", "nor", "slt", "sltu"] + ["sll", "srl", "sra"] + ["addi", "subi", "slti", "sltiu","andi", "ori", "xori", "lui"]

		self.line_mapping = {'line_no':[], 'pc_no':[], 'label':[], 'operation':[], 'arg1':[],'arg2':[],'arg3':[]}
		self.called_labels_mapping = {'line_no':[], 'pc_no':[], 'label':[]}
		self.bin = []
		self.errors = []
		self.warnings = []

		self.console = ''
		self.listing = ''
		self.bin = ''
		self.hex = ''
		self.operations = []

		self.console += '----assembler started----\n'

	def is_label(self, s, line_no) -> bool:
		if s[len(s)-1]==':':
			s = s[:-1]
			if str(s[0]).isalpha():
				if str(s).isalnum():
					return True
				else:
					print(s)
					self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tlabel name should not contail a special character\n')
					return False

			else:
				self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tlabel name should start with an alphabet\n')
		return False

	def is_register(self, s, line_no) -> bool:
		if s[0]=='$':
			s = s[1:]
			if s in self.register_mapper:
				if s in self.reserved_reg:
					self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tregister reserved for assembler\n')
				else:
					return True
			else:
				self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tno such register\n')
		else:
			self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error in register name\n')
		return False

	def is_offset_register(self, s, line_no) -> bool:
		off_reg = re.split(r'[()]', s)
		offset = off_reg[0]
		reg = off_reg[1]
		if(self.is_number(offset) and self.is_register(reg, line_no)):
			return True
		return False

	def is_number(self, s) -> bool:
		if s=='': return False
		if s[0]=='+' or s[0]=='-':
			s = s[1:]
			if str(s).isnumeric():
				return True
		elif str(s).isnumeric():
			return True
		return False

	def is_valid_three_arg(self, op, args, line_no, pc_no) ->bool:
		if(op in self.r_rest):
			rd = args[0][:-1]
			rt = args[1][:-1]
			rs = args[2]
			if (self.is_register(rd, line_no) and self.is_register(rt, line_no) and self.is_register(rs, line_no)):
				self.line_mapping['operation'].append(op)
				self.line_mapping['arg1'].append(rd)
				self.line_mapping['arg2'].append(rt)
				self.line_mapping['arg3'].append(rs)
				return True
		elif(op in self.r_shft):
			rt = args[0][:-1]
			rs = args[1][:-1]
			const = args[2]
			if (self.is_register(rt, line_no) and self.is_register(rs, line_no) and (self.is_number(const))):
				self.line_mapping['operation'].append(op)
				self.line_mapping['arg1'].append(rt)
				self.line_mapping['arg2'].append(rs)
				self.line_mapping['arg3'].append(const)
				return True
		elif op in self.i_type:
			rt = args[0][:-1]
			rs = args[1][:-1]
			const = args[2]
			if(self.is_register(rt, line_no) and self.is_register(rs, line_no) and (self.is_number(const))):
				self.line_mapping['operation'].append(op)
				self.line_mapping['arg1'].append(rt)
				self.line_mapping['arg2'].append(rs)
				self.line_mapping['arg3'].append(const)
				return True
		elif op == 'beq':
			rt = args[0][:-1]
			rs = args[1][:-1]
			off_label = args[2]
			if(self.is_register(rt, line_no) and self.is_register(rs, line_no)):
				self.line_mapping['operation'].append(op)
				self.line_mapping['arg1'].append(rt)
				self.line_mapping['arg2'].append(rs)
				self.line_mapping['arg3'].append(off_label)
				if(self.is_number(off_label)==False):
					self.called_labels_mapping['line_no'].append(line_no)
					self.called_labels_mapping['pc_no'].append(pc_no)
					self.called_labels_mapping['label'].append(off_label)
				return True
		return False

	def is_valid_two_arg(self, op, args, line_no, pc_no) -> bool:
		if op in self.ls_type:
			reg = args[0][:-1]
			off_reg = args[1]
			if(self.is_register(reg, line_no) and self.is_offset_register(off_reg, line_no)):
				self.line_mapping['operation'].append(op)
				self.line_mapping['arg1'].append(reg)
				self.line_mapping['arg2'].append(off_reg)
				self.line_mapping['arg3'].append('')
				return True
		elif op == 'beq':
			reg = args[0][:-1]
			off_label = args[1]
			if(self.is_register(reg, line_no)):
				self.line_mapping['operation'].append(op)
				self.line_mapping['arg1'].append(reg)
				self.line_mapping['arg2'].append(off_label)
				self.line_mapping['arg3'].append('')
				if(self.is_number(off_label)==False):
					self.called_labels_mapping['line_no'].append(line_no)
					self.called_labels_mapping['pc_no'].append(pc_no)
					self.called_labels_mapping['label'].append(off_label)
				return True
		return False

	def is_valid_one_arg(self, op, args, line_no, pc_no)->bool:
		if (op in ["j", "jal"]):
			label = args[0]
			self.line_mapping['operation'].append(op)
			self.line_mapping['arg1'].append(label)
			self.line_mapping['arg2'].append('')
			self.line_mapping['arg3'].append('')
			if(self.is_number(label)==False):
				self.called_labels_mapping['line_no'].append(line_no)
				self.called_labels_mapping['pc_no'].append(pc_no)
				self.called_labels_mapping['label'].append(label)
			return True
		elif (op in ["jr", "print"]):
			reg = args[0]
			if (self.is_register(reg, line_no)):
				self.line_mapping['operation'].append(op)
				self.line_mapping['arg1'].append(reg)
				self.line_mapping['arg2'].append('')
				self.line_mapping['arg3'].append('')
				return True
		return False

	def is_valid_no_arg(self, op, args, line_no, pc_no)->bool:
		if op in self.no_arg:
			self.line_mapping['operation'].append(op)
			self.line_mapping['arg1'].append('')
			self.line_mapping['arg2'].append('')
			self.line_mapping['arg3'].append('')
			return True
		return False

	def first_pass(self):
		line_no = 1
		pc_no = 0
		file_read = open(self.file_address, 'r')
		for line in file_read.readlines():
			line = line.strip()
			if line=='':
				line_no+=1
				continue
			if line[0]==';':
				line_no += 1
				continue
			words = re.split(' |\t', line)
			print(words)
			if len(words)>5:
				self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
				break
			else:
				self.line_mapping['line_no'].append(line_no)
				self.line_mapping['pc_no'].append(pc_no)
				if len(words)==5:
					if(self.is_label(words[0], line_no)):
						self.line_mapping['label'].append(words[0][:-1])
						if(self.is_valid_three_arg(words[1], words[2:], line_no, pc_no)):
							pass
						else:
							self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
							break
					else:
						self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
						break
					pc_no+=1

				elif len(words)==4:
					if(self.is_label(words[0], line_no)):
						self.line_mapping['label'].append(words[0][:-1])
						if(self.is_valid_two_arg(words[1], words[2:], line_no, pc_no)):
							pass
						else:
							self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
							break
					elif(self.is_valid_three_arg(words[0], words[1:], line_no, pc_no)):
						self.line_mapping['label'].append(None)
					else:
						self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
						break
					pc_no+=1

				elif len(words)==3:
					if(self.is_label(words[0], line_no)):
						self.line_mapping['label'].append(words[0][:-1])
						pc_no += 1
						if(self.is_valid_one_arg(words[1], words[2:], line_no, pc_no)):
							pass
						else:
							self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
							break
					elif(self.is_valid_two_arg(words[0], words[1:], line_no, pc_no)):
						self.line_mapping['label'].append(None)
					else:
						self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
						break
					pc_no+=1
				elif len(words)==2:
					if(self.is_label(words[0], line_no)):
						self.line_mapping['label'].append(words[0][:-1])
						if(self.is_valid_no_arg(words[1],  None, line_no, pc_no)):
							pass
						else:
							self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
							break
					elif(self.is_valid_one_arg(words[0], words[1:], line_no, pc_no)):
						self.line_mapping['label'].append(None)
					else:
						self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
						break
					pc_no+=1
				elif len(words)==1:
					if(self.is_label(words[0], line_no)):
						self.line_mapping['label'].append(words[0][:-1])
						self.line_mapping['operation'].append(None)
						self.line_mapping['arg1'].append('')
						self.line_mapping['arg2'].append('')
						self.line_mapping['arg3'].append('')
					elif(self.is_valid_no_arg(words[0], None, line_no, pc_no)):
						self.line_mapping['label'].append(None)
						pc_no+=1
					else:
						self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tsyntax error\n')
						pc_no+=1
						break

			line_no += 1

	def second_pass(self):
		if len(self.errors)==0:
			for i in range(len(self.called_labels_mapping['label'])):
				if self.called_labels_mapping['label'][i] not in self.line_mapping['label']:
					line_no = self.called_labels_mapping['line_no'][i]
					self.errors.append('ERROR:\tline:'+f'{line_no}'+'\tundefined label\n')
					break
			
			if len(self.errors)==0:
				for i in range(len(self.line_mapping['label'])):
					if self.line_mapping['label'][i] is not None:
						if self.line_mapping['label'][i] not in self.called_labels_mapping['label']:
							line_no = self.line_mapping['line_no'][i]
							self.warnings.append('WARNING:\tline:'+f'{line_no}'+'\tlabel not used\n')

					pc_no = self.line_mapping['pc_no'][i]
					bin_inst = ''
					hex_inst = ''
					op = ''
					label = ''
					
					if(self.line_mapping['label'][i] is not None):
						label = self.line_mapping['label'][i]
					if(self.line_mapping['operation'][i] is not None):
						op = self.line_mapping['operation'][i]
						bin_inst = self.opcode_mapper[op]
					else:
						continue
					arg1 = self.line_mapping['arg1'][i]
					arg2 = self.line_mapping['arg2'][i]
					arg3 = self.line_mapping['arg3'][i]

					self.listing += (f'{pc_no}'+'\t'+label+'\t'+op+'\t'+arg1+'\t'+arg2+'\t'+arg3+'\n')

					if op in self.r_rest:
						rs = arg2
						rt = arg3
						rd = arg1
						bin_inst += str(bin(self.register_mapper.index(rs[1:])))[2:].zfill(5)
						bin_inst += str(bin(self.register_mapper.index(rt[1:])))[2:].zfill(5)
						bin_inst += str(bin(self.register_mapper.index(rd[1:])))[2:].zfill(5)

						bin_inst += "00000"
						bin_inst += self.funct_mapper[op]

					if op in self.r_shft:
						rs = arg2
						rd = arg1
						shamt = str(bin(int(arg3)))[2:]

						bin_inst += str(bin(self.register_mapper.index(rs[1:])))[2:].zfill(5)
						bin_inst += str(bin(self.register_mapper.index(rt[1:])))[2:].zfill(5)
						bin_inst += str(bin(0))[2:].zfill(5)
						bin_inst += shamt.zfill(5)
						bin_inst += self.funct_mapper[op].zfill(6)

					if op in self.i_type:
						rt = arg1
						offset = arg3
						rs = arg2

						bin_inst += str(bin(self.register_mapper.index(rs[1:])))[2:].zfill(5)
						bin_inst += str(bin(self.register_mapper.index(rt[1:])))[2:].zfill(5)
						bin_inst += str(bin(int(offset)))[2:].zfill(16)

					if op in (["j","jal"]):
						l_offset = arg1
						offset = self.called_labels_mapping['pc_no'][(self.called_labels_mapping['label'].index(l_offset))] - self.line_mapping['pc_no'][(self.line_mapping['label'].index(l_offset))]
						bin_inst += str(bin(offset))[2:].zfill(26)

					if op in self.ls_type:
						off_reg = re.split(r'[()]', arg2)
						rt = arg1
						offset = off_reg[0]
						rs = off_reg[1]

						bin_inst += str(bin(self.register_mapper.index(rs[1:])))[2:].zfill(5)
						bin_inst += str(bin(self.register_mapper.index(rt[1:])))[2:].zfill(5)
						bin_inst += str(bin(int(offset)))[2:].zfill(16)


					if op == "beq":
						bin_inst = "000100"
						rs = arg1
						rt = arg2
						l_offset = arg3

						bin_inst += str(bin(self.register_mapper.index(rs[1:])))[2:].zfill(5)
						bin_inst += str(bin(self.register_mapper.index(rt[1:])))[2:].zfill(5)

						if l_offset not in self.called_labels_mapping['label']:
							print('hahaha')
							bin_inst += str(bin(l_offset))[2:].zfill(16)

						else:
							offset = (self.line_mapping['pc_no'][(self.line_mapping['label'].index(l_offset))]) - (self.called_labels_mapping['pc_no'][(self.called_labels_mapping['label'].index(l_offset))])
							if offset>=0:
								bin_inst += str(bin(offset))[2:].zfill(16)	
							else:
								bin_inst += str(bin(offset))[3:].zfill(16)			

						
					if op == "nop":
						bin_inst = "1"*32

					if op == "exit":
						bin_inst = "01011100"+"0"*24

					if op == "print":
						bin_inst = "010000"
						rs = arg1
						bin_inst += str(bin(self.register_mapper.index(rs[1:])))[2:].zfill(5)
						bin_inst += "0"*21

					print(bin_inst)
					hex_inst = ''
					hex_inst = hex(int(bin_inst, 2))[2:].zfill(8)
					print(hex_inst)
					
					self.bin += (bin_inst+'\n')
					self.hex += (hex_inst+'\n')


	def execution(self):
		self.first_pass()
		self.second_pass()

		for i in range(len(self.errors)):
			self.console += self.errors[i]
		for i in range(len(self.warnings)):
			self.console += self.warnings[i]

		self.operations = self.line_mapping['operation']
		
		self.console += ('ERRORS:'+f'{len(self.errors)}'+'\tWARNINGS:'+f'{len(self.warnings)}'+'\n')
		self.console += '----assembler done----\n'

# x = assembler('/home/sanskriti/CS322_mini_project/testing/add_10_numbers.asm').execution()