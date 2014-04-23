import wikipydia
import urllib
from bs4 import BeautifulSoup, NavigableString, Comment
import sys
import nltk.data
from nltk import wordpunct_tokenize
from nltk import TreebankWordTokenizer
import optparse

optparser = optparse.OptionParser()
optparser.add_option("-l", "--language", dest="language", default="en", help="language of articles to look for")
(opts, args) = optparser.parse_args()

if opts.language == "en":
	titles = open("data/titles_enu.dev")
elif opts.language == "es":
	titles = open("data/titles_esn.dev")

def getContents(html):
	soup = BeautifulSoup(html)
	numSiblings = len(soup.contents)
	for i in range(0, numSiblings):
		currSib = soup.contents[i]
		if isinstance(currSib, NavigableString):
			if isinstance(currSib, Comment):
				s = ""
			else:
				s = unicode(currSib)
		elif currSib.name == "table" or (currSib.name == "div" and ((currSib.get('class') != None and currSib['class'][0][0:5] != "thumb") or currSib.get('class') == None)) :
			s = ""
		else:
			s = ""
			if currSib.name == "a" and currSib['href'][1:5] == "wiki":
				s += " [" + currSib['href'][6:] + "] "
			for c in currSib.contents:
				tagName = c.name;
				c = unicode(c)
				c = getContents(c)
				s += unicode(c)
				if(tagName == "li") :
					s += " li."
			if(currSib.get('class') != None and currSib['class'][0] == "thumbcaption") :
				s += " thumbcaption."
		currSib.replaceWith(s)
	return soup

for article in titles:
	(title, revID) = article.split("|||")
	(title, revID) = (title.strip(), revID.strip())
	html = wikipydia.query_text_rendered_by_revid(revID, opts.language)['html']
	pretty = BeautifulSoup(html)
	wiki_content = str(getContents(unicode(html)))
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = sent_detector.tokenize(wiki_content)
	tokenized_sentences = []
	for sentence in sentences:
		tokens = TreebankWordTokenizer().tokenize(sentence) 
		new_tokens = []
		seenEdit = False
		seenLi = False
		seenCapt = False
		isCloseParen = False
		for token in tokens:
			#doesn't work for nested quotes
			if token == "\"" and not isCloseParen:
				token = "``"
				isCloseParen = True
			if token == "\"" and isCloseParen:
				token = "''"
				isCloseParen = False
			if "(" in token:
				index = token.index("(")
				token = token[:index] + " -LRB- " + token[index + 1:]
			if ")" in token:
				index = token.index(")")
				token = token[:index] + " -RRB- " + token[index + 1:]
			if (opts.language == "en" and token == "edit") or (opts.language == "es" and token == "editar"):
				seenEdit = True
			if token == "]" and seenEdit:
				token = "] \n"
				seenEdit = False
			if token == "li":
				seenLi = True
				token = ""
			if token == "thumbcaption":
				seenCapt = True
				token = ""
			if token == "." and (seenLi or seenCapt):
				seenLi = False
				seenCapt = False
				token = ""
			if "[" in token and token != "[":
				ind = token.index("[")
				token = token[:ind] + " " + token[ind:]
			new_tokens.append(token)
		new_sent = ' '.join(new_tokens).strip()
		if new_sent != "":
			tokenized_sentences.append(new_sent)
	tokenized_sentences.insert(0, title)
	print '\n'.join([t for t in tokenized_sentences]) + '\n'
