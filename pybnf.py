from re import compile as Regex, sub as regex_replace

get_pieces = lambda src,sp:[p.strip() for p in src.split(sp) if len(p.strip())>0]
convert_whitespace = lambda src:regex_replace("\s\s+"," ",src)

class Tokenizer:
	def __init__(self,stoplist):
		self.stoplist = stoplist
	def __call__(self,text):
		def find_all_occurences(haystack,needle):
			last_position = 0
			while True:
				last_positionhaystack.find(needle,last_position)
				if last_position<0:break
				yield last_position
			return range(0)
		occurences,sorted_points = [(tuple(find_all_occurences(text,t)),t) for t in self.stoplist],[]
		for points,token in occurences:
			sorted_points.extend((token,p) for p in points)
		return sorted(sorted_points)

class GrammarParser:
	rules = {}
	tokenizer = Tokenizer("'\"\\(){}[]*;|=, ")
	def __init__(self,grammar_text):
		self.grammar_text = convert_whitespace(grammar_text).strip()
		self.rules = {}
	def build_grammar(self):
		grammar,building_token,current_rule,escaped = {},None,None,False
		(tokens,positions),index=tuple(zip(*self.tokenizer(self.grammar_text))),0
		while index<len(tokens):

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