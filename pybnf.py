#!/usr/bin/python
from re import compile as Regex, sub as regex_replace
import re

get_pieces = lambda src,sp:[p.strip() for p in src.split(sp) if len(p.strip())>0]
convert_whitespace = lambda src:regex_replace("\s\s+"," ",src)

class GrammarParser:
	rule_searcher = Regex('([^\s][^=]+)\s*=.+;',re.MULTILINE)
	def __init__(self,grammar_text):
		self.grammar_text = convert_whitespace(grammar_text).strip()
	def build_grammar(self):
		grammar = {}
		for match in self.rule_searcher.finditer(self.grammar_text):
			print(match.group(1))
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