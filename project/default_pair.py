import optparse
import sys

optparser = optparse.OptionParser()
optparser.add_option("-e", "--english", dest="e", default="test/orig.enu.test", help="english wikipedia article")
optparser.add_option("-f", "--foreign", dest="f", default="test/orig.esn.test", help="foreign wikipedia article")
(opts, args) = optparser.parse_args()

e_sentences = open(opts.e, "r")
f_sentences = open(opts.f, "r")


e_line = e_sentences.readline()
f_line = f_sentences.readline()

while e_line and f_line:
	
	english = []

	while len(e_line.strip()) != 0:
		english.append(e_line)
		e_line = e_sentences.readline()
	e_line = e_sentences.readline()

	i = 0
	while len(f_line.strip()) != 0:
		if i < len(english):
			print english[i].strip() + " ||| " + f_line.strip()
		f_line = f_sentences.readline()
		i += 1
	f_line = f_sentences.readline()


