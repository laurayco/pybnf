from re import compile as Regex, sub as regex_replace

get_pieces = lambda src,sp:[p.strip() for p in src.split(sp) if len(p.strip())>0]
convert_whitespace = lambda src:regex_replace("\s\s+"," ",src)

class Tokenizer:
	def __init__(self,stoplist):
		self.stoplist = stoplist
	def __call__(self,text):
		position,end = 0, len(text)
		while position<end:
			start = position
			while text[position] not in self.stoplist:
				position+=1
			else:
				yield text[position],None
			if position>start:
				yield text[position],text[start:position]
			position += 1

class GrammarParser:
	rules = {}
	tokenizer = Tokenizer("'\"(){}[]*;|=, ")
	def __init__(self,grammar_text):
		self.grammar_text = convert_whitespace(grammar_text)
		for token, data in self.tokenizer(self.grammar_text):
			print(token,data)
		self.rules = {}

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