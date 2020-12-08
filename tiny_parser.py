"""
4th CSE - FoE ASU
System Software (Compilers)
Project 2: TINY Parser

Team Members:
	Pierre Nabil
	Girgis Michael
	John Bahaa
	Hazem Mohammed
"""

# Imports
import ete3
from parserError import MatchingError


# Reader Class
class TokenReader:
	def __init__(self, filename):
		self.file = open(filename, 'r')
		self.last_token = None

	def _gettoken(self):
		line = self.file.readline()
		if line:
			return line.rstrip().split(',')
		else:
			raise EOFError('Reached EOF.')

	def peek(self):
		if self.last_token is None:
			next_token_text, next_token_type = self._gettoken()
			self.last_token = next_token_text, next_token_type
		return self.last_token

	def match(self, token_type):
		if self.last_token is not None:
			next_token_text, next_token_type = self.last_token
		else:
			next_token_text, next_token_type = self._gettoken()
		if next_token_type != token_type:
			raise MatchingError(token_type, next_token_type)
		else:
			self.last_token = None
		return next_token_text, next_token_type

	def match_any(self, token_type_list):
		if self.last_token is None:
			self.peek()
		any_match = False
		next_token_text, next_token_type = self.last_token
		for token_type in token_type_list:
			try:
				self.match(token_type)
			except MatchingError:
				continue
			else:
				any_match = True
				break
		if any_match:
			self.last_token = None
			return next_token_text, next_token_type
		else:
			raise MatchingError(token_type_list, next_token_type)


class Parser:
	def __init__(self, filename='data/token_list.txt'):
		self.reader = TokenReader(filename)

		self.last_inner_tree = '', ''
		self.s_tree_str = ''
		self.s_tree = None

		self.p_tree_str = ''
		self.p_tree = None

		self.tree_style = None

	def save(self, s_tree_filename='mySyntaxtree.png', p_tree_filename='myParsetree.png'):
		if self.s_tree is None:
			raise Exception('Must use parse_tokens first.')
		self.s_tree.render(s_tree_filename, units="mm", tree_style=self.tree_style, dpi=600)
		self.p_tree.render(p_tree_filename, units='mm', tree_style=self.tree_style, dpi=600)

	def show(self, show_parse=True, show_syntax=True):
		if self.s_tree is None:
			raise Exception('Must use parse_tokens first.')
		if show_parse:
			self.p_tree.show(tree_style=self.tree_style)
		if show_syntax:
			self.s_tree.show(tree_style=self.tree_style)

	def _create_graph_layout(self):
		ns = ete3.NodeStyle()
		ts = ete3.TreeStyle()

		def my_layout(node):
			name_face = ete3.AttrFace("name", fsize=12)
			name_face.border.width	= 1
			name_face.margin_left	= 10
			name_face.margin_right	= 10
			name_face.margin_top	= 5
			name_face.margin_bottom	= 5

			ns['fgcolor'] = 'Black'
			ns['shape'] = 'square'
			ns['size'] = 7

			ete3.faces.add_face_to_node(name_face, node, column=0, position="branch-right")
			node.set_style(ns)

		ts.show_leaf_name = False
		ts.layout_fn = my_layout
		ts.show_border = True
		ts.show_scale = False
		ts.min_leaf_separation = 40
		ts.margin_top = 30
		ts.margin_bottom = 30
		ts.margin_left = 40
		ts.margin_right = 40

		self.tree_style = ts

	def parse_tokens(self, print_tree_string=False):
		# program = stmt_seq
		inner_tree = self._stmt_seq(True)

		if inner_tree == ('', ''):
			self.s_tree_str = self.p_tree_str = 'program;'
		else:
			self.s_tree_str = '(' + inner_tree[1] + ')program;'
			self.p_tree_str = '(' + inner_tree[0] + ')program;'

		if print_tree_string:
			print('Syntax Tree String:\n')
			print(self.s_tree_str)
			print('Parse Tree String:')
			print(self.p_tree_str)

		self.s_tree = ete3.Tree(self.s_tree_str, format=8)
		self.p_tree = ete3.Tree(self.p_tree_str, format=8)

		self._create_graph_layout()

	def _stmt_seq(self, root=False):
		# stmt_seq = stmt {; stmt}
		# Doesn't Appear in Syntax Tree IF only one stmt
		only_stmt = True
		try:
			first_tree = self._stmt()
		except EOFError:
			return '', ''
		inner_tree = [first_tree[0], '']
		while True:
			try:
				self.reader.peek()
				self.reader.match('SEMI')
			except MatchingError:
				break
			except EOFError as err:
				if root:
					print(err.args[0])
					break
				else:
					raise err
			only_stmt = False
			try:
				inner_p, inner_s = self._stmt()
				inner_tree[0] = '(' + inner_tree[0] + ')stmt_seq,SEMI,' + inner_p
				inner_tree[1] += ',' + inner_s
			except EOFError as err:
				if root:
					print(err.args[0])
					break
				else:
					raise err

		if only_stmt:
			s_str = first_tree[1]
		else:
			s_str = '(' + first_tree[1] + inner_tree[1] + ')stmt_seq'
		p_str = '(' + inner_tree[0] + ')stmt_seq'

		return p_str, s_str

	def _stmt(self):
		# stmt = if_stmt | repeat_stmt | read_stmt | write_stmt | assign_stmt
		# Doesn't appear in Syntax Tree
		try:
			self.reader.peek()
			p_str, s_str = self._if_stmt()
		except MatchingError:
			try:
				p_str, s_str = self._repeat_stmt()
			except MatchingError:
				try:
					p_str, s_str = self._read_stmt()
				except MatchingError:
					try:
						p_str, s_str = self._write_stmt()
					except MatchingError:
						try:
							p_str, s_str = self._assign_stmt()
						except MatchingError as err:
							next_token_type = err.found_token
							raise MatchingError(['IF', 'REPEAT', 'READ', 'WRITE', 'ID'], next_token_type)
		p_str = '(' + p_str + ')stmt'
		return p_str, s_str

	def _if_stmt(self):
		# if_stmt = if exp then stmt_seq [else stmt_seq] end
		self.reader.match('IF')
		cond_str = self._exp()
		self.reader.match('THEN')
		then_str = self._stmt_seq()
		s_str = cond_str[1] + ',' + then_str[1]
		p_str = 'IF"if",' + cond_str[0] + ',THEN"then",' + then_str[0]
		try:
			self.reader.peek()
			self.reader.match('ELSE')
		except MatchingError:
			pass
		else:
			else_str = self._stmt_seq()
			s_str += ',' + else_str[1]
			p_str += ',ELSE"else",' + else_str[0]
		self.reader.match('END')

		s_str = '(' + s_str + ')if_stmt'
		p_str = '(' + p_str + ',END"end")if_stmt'
		return p_str, s_str

	def _repeat_stmt(self):
		# repeat_stmt = repeat stmt_seq until exp
		self.reader.match('REPEAT')
		repeat_str = self._stmt_seq()
		self.reader.match('UNTIL')
		cond_str = self._exp()

		s_str = '(' + repeat_str[1] + ',' + cond_str[1] + ')repeat_stmt'
		p_str = '(REPEAT"repeat",' + repeat_str[0] + ',UNTIL"until",' + cond_str[0] + ')repeat_stmt'
		return p_str, s_str

	def _read_stmt(self):
		# read_stmt = read id
		self.reader.match('READ')
		next_token_text, next_token_type = self.reader.match('ID')

		s_str = '(ID"' + next_token_text + '")read_stmt'
		p_str = '(READ"read",ID"' + next_token_text + '")read_stmt'
		return p_str, s_str

	def _write_stmt(self):
		# write_stmt = write exp
		self.reader.match('WRITE')
		exp = self._exp()

		s_str = '(' + exp[1] + ')write_stmt'
		p_str = '(WRITE"write",' + exp[0] + ')write_stmt'
		return p_str, s_str

	def _assign_stmt(self):
		# assign_stmt = id:= exp
		next_token_text, next_token_type = self.reader.match('ID')
		id_str = 'ID"' + next_token_text + '"'

		self.reader.match('ASSIGN')
		exp_str = self._exp()

		s_str = '(' + id_str + ',' + exp_str[1] + ')assign_stmt'
		p_str = '(' + id_str + ',ASSIGN,' + exp_str[0] + ')assign_stmt'
		return p_str, s_str

	def _exp(self):
		# exp = simple_exp [comp_op simple_exp]
		# Doesn't Appear in Syntax Tree IF only one simple_exp
		only_stmt = True
		first_tree = self._simple_exp()
		second_tree = ''
		try:
			self.reader.peek()
			next_token_text, next_token_type = self._comp_op()
		except MatchingError:
			pass
		except EOFError:
			pass
		else:
			only_stmt = False
			second_tree = self._simple_exp()

		if only_stmt:
			s_str = first_tree[1]
			p_str = '(' + first_tree[0] + ')exp'
		else:
			s_str = '(' + first_tree[1] + ',' + second_tree[1] + ')exp"' + next_token_text + '"'
			p_str = '(' + first_tree[0] + ',' + next_token_type + '"' + next_token_text + '",' + second_tree[0] + ')exp'

		return p_str, s_str

	def _simple_exp(self):
		# simple_exp = term {add_op term}
		# Doesn't Appear in Syntax Tree IF only one term
		only_stmt = True
		first_tree = self._term()
		inner_tree = [first_tree[0], '']
		while True:
			try:
				self.reader.peek()
				next_token_text, next_token_type = self._add_op()
			except MatchingError:
				break
			except EOFError:
				break
			else:
				only_stmt = False
				inner_p, inner_s = self._term()
				inner_tree[1] += ',' + inner_s
				inner_tree[0] = '(' + inner_tree[0] + ')simple_exp,' + next_token_type + '"' + next_token_text + '",' + inner_p

		if only_stmt:
			s_str = first_tree[1]
		else:
			s_str = '(' + first_tree[1] + inner_tree[1] + ')simple_exp"' + next_token_text + '"'

		p_str = '(' + inner_tree[0] + ')simple_exp'
		return p_str, s_str

	def _term(self):
		# term = factor {mul_op factor}
		# Doesn't Appear in Syntax Tree IF only one factor
		only_stmt = True
		first_tree = self._factor()
		inner_tree = [first_tree[0], '']
		while True:
			try:
				self.reader.peek()
				next_token_text, next_token_type = self._mul_op()
			except MatchingError:
				break
			except EOFError:
				break
			else:
				only_stmt = False
				inner_p, inner_s = self._factor()
				inner_tree[1] += ',' + inner_s
				inner_tree[0] = '(' + inner_tree[0] + ')term,' + next_token_type + '"' + next_token_text + '",' + inner_p

		if only_stmt:
			s_str = first_tree[1]
		else:
			s_str = '(' + first_tree[1] + inner_tree[1] + ')term"' + next_token_text + '"'

		p_str = '(' + inner_tree[0] + ')term'
		return p_str, s_str

	def _factor(self):
		# factor = ( exp ) | num | id
		# Doesn't Appear in Syntax Tree IF ( exp )
		self.reader.peek()
		matched_token_text, matched_token_type = self.reader.match_any(['LBRACKET', 'NUM', 'ID'])
		if matched_token_type == 'LBRACKET':
			exp = self._exp()
			s_str = exp[1]
			p_str = '(LBRACKET,' + exp[0] + ',RBRACKET)factor'
			self.reader.match('RBRACKET')
		elif matched_token_type == 'ID':
			s_str = 'ID"' + matched_token_text + '"'
			p_str = '(' + s_str + ')factor'
		else: #for NUM
			s_str = 'NUM"' + matched_token_text + '"'
			p_str = '(' + s_str + ')factor'

		return p_str, s_str

	def _comp_op(self):
		# comp_op = < | > | =
		return self.reader.match_any(['LT', 'GT', 'EQ'])

	def _add_op(self):
		# add_op = + | -
		return self.reader.match_any(['ADD', 'SUB'])

	def _mul_op(self):
		# mul_op = * | /
		return self.reader.match_any(['MUL', 'DIV'])


if __name__ == '__main__':
	parser = Parser()
	parser.parse_tokens(True)
	parser.show()
	parser.save()
