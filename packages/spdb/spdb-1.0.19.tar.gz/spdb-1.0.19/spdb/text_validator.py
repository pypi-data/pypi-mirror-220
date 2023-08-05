import re


class TextValidator:
	def __init__(self, min: int=4, max: int=64, regexp: str=r'([A-z]|[0-9]|_|-)+'):
		self.min = min
		self.max = max
		self.regexp = regexp


	def check(self, text: str):
		if re.sub(self.regexp, '', text) != '':
			return False
		if len(text) > self.max or len(text) < self.min:
			return False
		return True