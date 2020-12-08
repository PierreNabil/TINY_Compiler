"""
4th CSE - FoE ASU
System Software (Compilers)
Project 2: TINY Parser

Helper Module for Error Handeling

Team Members:
	Pierre Nabil
	Girgis Michael
	John Bahaa
	Hazem Mohammed
"""


class Error(Exception):
	pass


class MatchingError(Error):
	def __init__(self, expected_token, found_token):
		self.expected_token = str(expected_token)
		self.found_token    = str(found_token)

	# use like this:
	# except MatchingError as err:
	#	 print(err)
	def __str__(self):
		return 'Expected Token: ' + self.expected_token + ' Found: ' + self.found_token