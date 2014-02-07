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
			while text[position] not in self.stoplist: position+=1
			else: yield text[position],None
			if position>start: yield text[position],text[start:position]
			position += 1

class GrammarParser:
	rules = {}
	tokenizer = Tokenizer("'\"(){}[]*;|=, ")
	def __init__(self,grammar_text):
		self.grammar_text = convert_whitespace(grammar_text)
		self.rules = {}
	def build_grammar(self):
		grammar,building_token,current_rule = {},None,None
		for token, data in self.tokenizer(self.grammar_text):
			if token==' ':
				if building_token is not None:
					if data is None: building_token += ' '
					else: building_token += data
				elif data is not None: building_token = data
			elif token=='=':#the currently building token must be a rule name.
				current_rule = building_token.strip()
				grammar[current_rule] = [[]]
				building_token = None
			elif token=='|':
				grammar[current_rule].append([])
			elif token==';':
				current_rule = None
			elif token=='"':
				if building_token is not None:#closing a string.
					building_token += (data.rstrip() if data is not None else "") + '"'
					print("Closing literal:",building_token)
				else:
					print("Opening literal.")
					building_token = '"'
			elif token==',':
				if data is not None and building_token is not None:
					building_token+=data.rstrip()
				grammar[current_rule][-1].append(building_token)
				building_token = None
		return grammar

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
	grammar = GrammarParser(sample_ebnf).build_grammar()
	from json import dump;dump(grammar,open("parsed.json",'w'),indent=2,sort_keys=True)