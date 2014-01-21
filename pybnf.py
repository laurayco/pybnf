from re import compile as Regex, sub as regex_replace

get_pieces = lambda src,sp:[p.strip() for p in src.split(sp) if len(p.strip())>0]
convert_whitespace = lambda src:regex_replace("\s\s+"," ",src)

class Token:
	LITERAL_START = '"'
	LITERAL_END = '"'
	COMMENT_START = '(*'
	COMMENT_END = '*)'
	REPEAT_START = '{'
	REPEAT_END = '}'
	OPTION_START = '['
	OPTION_END = ']'
	TOKEN_SEPERATOR = ','
	def __init__(self,rule):
		self.grammar = rule
		sub_tokens = self.tokenify(rule)
		self.sub_tokens = sub_tokens
	@classmethod
	def tokenify(cls,rule):
		rule = rule.strip()
		lr = len(rule)
		current_token = None
		token_start, token_end = 0,0
		while token_start < lr and token_end < lr:
			if current_token=='comment':
				if rule[token_end:token_end+len(cls.COMMENT_END)]==cls.COMMENT_END:
					yield current_token,rule[token_start:token_end]
					token_start = token_end + len(cls.COMMENT_END)
					token_end = token_start
					current_token = None
			if current_token=='literal':
				if rule[token_end:token_end+len(cls.LITERAL_END)]==cls.LITERAL_END:
					yield current_token,rule[token_start:token_end]
					token_start = token_end + len(cls.LITERAL_END)
					token_end = token_start
					current_token = None
			if current_token=='repeated':
				if rule[token_end:token_end+len(cls.REPEAT_END)]==cls.REPEAT_END:
					yield current_token,list(cls.tokenify(rule[token_start:token_end]))
					token_start = token_end + len(cls.REPEAT_END)
					token_end = token_start
					current_token = None
			if current_token=='optional':
				pass

	@classmethod
	def make_sub_token(cls,token):
		def open_close(s,a,b): return s[:len(a)]==a and s[len(s)-len(b):]==b
		if open_close(token,cls.COMMENT_START,cls.COMMENT_END):
			return 'comment',token[len(cls.COMMENT_START):len(token)-len(cls.COMMENT_END)]
		if open_close(token,cls.LITERAL_START,cls.LITERAL_END):
			return 'literal',token[len(cls.LITERAL_START):len(token)-len(cls.LITERAL_END)]
	def __str__(self):
		return self.grammar
	def __call__(self,match_info):
		pass

class Grammar:
	RULE_SEPARATOR = ';'
	RULE_DEFINITION_INDICATOR = '='
	DEFINITION_ALTERNATION = '|'
	TokenType = Token
	def __init__(self,grammar_text):
		grammar_text = get_pieces(grammar_text,self.RULE_SEPARATOR)
		rules = map(self.seperate_rule,grammar_text)
		rules = map(self.build_definition,*zip(*rules))
		self.rules = dict(rules)
	@classmethod
	def build_definition(cls,rule_name,rule_definition):
		definitions = get_pieces(convert_whitespace(rule_definition),cls.DEFINITION_ALTERNATION)
		return rule_name, list(map(cls.TokenType,definitions))
	@classmethod
	def seperate_rule(cls,rule_line):
		#reduce whitespace to a minimum.
		rule_line = convert_whitespace(rule_line)
		definition_point = rule_line.find(cls.RULE_DEFINITION_INDICATOR)
		rule_name = rule_line[:definition_point].strip()
		rule_definition = rule_line[definition_point+1:].strip()
		return rule_name, rule_definition

class GrammarParse:
	def __init__(self,grammar,src):
		self.source = src
		self.position = 0
		self.grammar = grammar
	@property
	def remaining_data(self):
		return self.source[self.position:]

def parse_ebnf(ebnf):
	ebnf = convert_whitespace(ebnf).strip()
	start,end=0,0
	max_pos=len(ebnf)
	is_good = lambda s,e:s<max_pos and e<max_pos
	def skip_until(s,p,*m,invert=False):
		condition = (lambda t,p,s:s[p:p+len(t)]!=t)
		if invert:condition = (lambda t,p,s:s[p:p+len(t)]==t)
		while any(condition(t,p,s) for t in m):p+=1
		return p
	while is_good(start,end):
		#skip white-space.
		start = skip_until(ebnf,start,' ',invert=True)
		#find the end of the rule-name.
		end = skip_until(ebnf,start,'=')
		rule_name = ebnf[start:end].strip()
		#we can't assume that this thing 
		start = end = skip_until(ebnf,end,'=') + 1
		print(ebnf[start:])
		#now that we have the rule, find the definitions.
		definitions = []
		while is_good(start,end):
			print(ebnf[start:])
			start = skip_until(ebnf,start,' ',invert=True)
			if ebnf[start]=='(':
				start+=1
				if ebnf[start]=='*':#it's a comment.
					end = skip_until(ebnf,start,'*)')
					print("Identified comment:",ebnf[start:end])
		yield rule_name, definitions
		start = end

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
	#grammar = Grammar(sample_ebnf)
	#for rule,definitions in grammar.rules.items():
	#	print("Rule","'" + rule + "'","has the following definitions:")
	#	for definition in definitions:
	#		print("\t",definition)
	#	print("="*80)
	parse_ebnf(sample_ebnf)