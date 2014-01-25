from re import compile as Regex, sub as regex_replace

get_pieces = lambda src,sp:[p.strip() for p in src.split(sp) if len(p.strip())>0]
convert_whitespace = lambda src:regex_replace("\s\s+"," ",src)

def parse_definition(defi):
	#I know this won't be accessed often,
	# but just in case it is, I'm ensuring
	# that the definition is stripped
	# and reduced for whitespace.
	defi = convert_whitespace(defi).strip()
	start,end,last = 0,0,len(defi)
	while start<last and end < last:
		# An alternation creates a new yield.
		#  A sub-group creates a new list.
		#  A comment is ignored.
		#  A literal marked with double-quotes ("")
		#    will be interpreted as a literal literal.
		#  A literal marked with single-quotes ('')
		#    will be interpreted as a regex literal.
		#  Anything else will be read as a reference
		#    to a different rule.
		#  A (), {}, or [] denotes a sub-set of tokens.
		#    They will be yielded as either 'sub', 'repeated', or 'optional' and an
		#    generator of the sub-set.
	return range(0)

class GrammarParser:
	def __init__(self,lang):
		# remove redundant whitespace, and normalize it into a single space.
		lang = convert_whitespace(lang).strip()
		token_searches = '= , | { } (* *) ( ) [ ] ;'.split()
		end_states = [
			self.create_rule,
			self.sequence_token,
			self.alternate_definition,
			self.start_repeating,
			self.end_repeating,
			self.start_comment,
			self.end_comment,
			self.start_group,
			self.end_group,
			self.start_optional,
			self.end_optional,
			self.end_rule
		]
		self.state,escaped,position,piece_start = 0,False,0,0
		while position < len(lang):
			tok = token_searches[self.state]
			if lang[position:position+len(tok)]==tok and not escaped:
				self.state = end_states[self.state](lang[current_piece[0]:position])
				piece_start = position = position + 1

if __name__=="__main__":
	sample_ebnf = """
		digit excluding zero = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
		digit                = "0" | digit excluding zero, (* Realistically we wouldn't want this to repeat. *);
		addition operator    = "+";
		subtraction operator = "-";
		multiplication operator = "*";
		division operator    = "/";
		mathematic operator = multiplication operator | division operator | addition operator | subtraction;
		mathematic expression = number, mathematic operator, number;
		number = digit | mathematic expression;
	"""
	def display_definition(defin):
		#As the definition variable increases in complexity,
		# So will this.
		print('\t->',defin,sep='')
	grammar = GrammarParser(sample_ebnf)
	for name, definition in grammar.rules.items():
		print("Rule",name,end=':\n')
		display_definition(definition)