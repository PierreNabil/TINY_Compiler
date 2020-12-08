"""
4th CSE - FoE ASU
System Software (Compilers)
Project 1: TINY Scanner

Team Members:
	Pierre Nabil
	Girgis Michael
	John Bahaa
	Hazem Mohammed
"""

# Imports
import os
from string import ascii_letters, whitespace

# Define Global Data
digits = set(str(i) for i in range(10))
letters = set(ascii_letters)
whitespace = set(whitespace)
special_symbols = {'+', '-', '*', '/', '=', '<', '>', '(', ')', ';'}

tiny_tokens = {
	'if'	: 'IF',
	'then'	: 'THEN',
	'else'	: 'ELSE',
	'end'	: 'END',
	'repeat': 'REPEAT',
	'until'	: 'UNTIL',
	'read'	: 'READ',
	'write'	: 'WRITE',

	'+'		: 'ADD',
	'-'		: 'SUB',
	'*'		: 'MUL',
	'/'		: 'DIV',
	'='		: 'EQ',
	'<'		: 'LT',
	'>'		: 'GT',
	'('		: 'LBRACKET',
	')'		: 'RBRACKET',
	';'		: 'SEMI',
	':='	: 'ASSIGN',

	'num'	: 'NUM',
	'id'	: 'ID'
}


# Main Function
def scan_file(input_filename, output_filename):
	with open(output_filename, 'w') as output_file:
		with open(input_filename, 'rb') as input_file:
			state = 'start'
			current_token_text = ''
			current_token_type = ''
			current_num_state = ''

			while True:
				char = input_file.read(1).decode("utf-8")
				# if EOF: end program
				if not char:
					if current_token_type in tiny_tokens.keys():
						output_string = '{},{}'.format(current_token_text, tiny_tokens[current_token_type])
						output_file.write(output_string + '\n')
						# print(output_string)
						state = 'start'
						current_token_text = ''
						current_token_type = ''
						current_num_state  = ''
					print("Finished Scanning!")
					break

				# States for FSM
				if state == 'start':
					if char == '{':
						state = 'in_comment'
					elif char == ':':
						state = 'in_assign'
					elif char in letters or char == '_':
						state = 'in_id'
						current_token_text = char
						current_token_type = 'id'
					elif char in digits or char == '.':
						state = 'in_num'
						current_token_text = char
						current_token_type = 'num'
						if char == '.':
							current_num_state = 'fraction_part'
						else:
							current_num_state = 'integer_part'
					elif char in special_symbols: # if char is an operator
						state = 'done'
						current_token_text = char
						current_token_type = char
					elif char in whitespace:
						continue
					else:
						print('Error: Unknown Character', char)
						break

				elif state == 'in_comment':
					if char == '}':
						state = 'start'
						# else: stay in this state

				elif state == 'in_num':
					if current_num_state == 'integer_part':
						if char in digits:
							current_token_text += char
						elif char == '.':
							current_token_text += char
							current_num_state = 'fraction_part'
						elif char in ['e' or 'E']:
							current_token_text += char
							# Cheat by reading the next sign of the exponent (unclean)
							char = input_file.read(1).decode("utf-8")
							if char in ['+', '-']:
								current_token_text += char
							else:
								input_file.seek(-1, os.SEEK_CUR)
							current_num_state = 'exponent_part'
						else:
							input_file.seek(-1, os.SEEK_CUR)
							state = 'done'
					elif current_num_state == 'fraction_part':
						if char in digits :
							current_token_text += char
						elif char in ['e' or 'E'] :
							current_token_text += char
							# Cheat by reading the next sign of the exponent (unclean)
							char = input_file.read(1).decode("utf-8")
							if char in ['+', '-'] :
								current_token_text += char
							else :
								input_file.seek(-1, os.SEEK_CUR)
							current_num_state = 'exponent_part'
						else:
							input_file.seek(-1, os.SEEK_CUR)
							state = 'done'
					elif current_num_state == 'exponent_part':
						if char in digits:
							current_token_text += char
						else:
							input_file.seek(-1, os.SEEK_CUR)
							state = 'done'
					else:
						print('Error: Unknown Number State', current_num_state)
						break

				elif state == 'in_id':
					if char in letters or char in digits or char == '_':
						current_token_text += char
					else:
						input_file.seek(-1, os.SEEK_CUR)
						state = 'done'
						# for reserved words
						if current_token_text in tiny_tokens.keys() and current_token_text not in ['num', 'id']:
							current_token_type = current_token_text

				elif state == 'in_assign':
					if char == '=':
						state = 'done'
						current_token_text = ':='
						current_token_type = ':='
					else:
						print('Error: Unknown Operator :', char, sep='')
						break

				else:
					print('Error: Unknown State', state)
					break

				# if we finished a Token
				if state == 'done':
					if current_token_type in tiny_tokens.keys():
						output_string = '{},{}'.format(current_token_text, tiny_tokens[current_token_type])
						output_file.write(output_string + '\n')
						# print(output_string)
						state = 'start'
						current_token_text = ''
						current_token_type = ''
						current_num_state  = ''
					else:
						print('Error: Unknown Token Type', current_token_type)
						break



if __name__ == '__main__':
	ip_filename = 'sample_code.txt'
	op_filename = 'token_list.txt'
	scan_file(ip_filename, op_filename)
