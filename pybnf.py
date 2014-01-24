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

def parse_ebnf(lang):
	# remove redundant whitespace, and normalize it into a single space.
	lang = convert_whitespace(lang).strip()
	current_rule,state = {
		'name':[0,0],
		'definition':[]
	},'finding name'
	for c in lang:
		if state=='finding name':
			if c=='=':
				state='building definition':
				break
			else:
				current_rule['name']+=c#add the character to the name.


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

	for name, definition in parse_ebnf(sample_ebnf):
		print("Rule",name,end=':\n')
		display_definition(definition)