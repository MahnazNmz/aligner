import optparse

optparser = optparse.OptionParser()
optparser.add_option("-e", "--english_pairs", dest="english_pairs", default="data/pairs.enu.dev", help="english pairs")
optparser.add_option("-f", "--foreign_pairs", dest="foreign_pairs", default="data/pairs.esn.dev", help="foreign pairs")
optparser.add_option("-o", "--one_grams", dest="one_grams", default="data/1_grams", help="one gram tanslation table")
optparser.add_option("-t", "--two_grams", dest="two_grams", default="data/2_grams", help="two gram translation table")
(opts, args) = optparser.parse_args()

result = open("pairs_withFeatures.txt", "w")

e_sentences = open(opts.english_pairs, "r")
f_sentences = open(opts.foreign_pairs, "r")

#pair up article sentences and add length_diff feature
e_line = e_sentences.readline()
f_line = f_sentences.readline()

while e_line and f_line:
	
	english = []

	while len(e_line.strip()) != 0:
		english.append(e_line.strip())
		e_line = e_sentences.readline()
	e_line = e_sentences.readline()

	while len(f_line.strip()) != 0:
		for e_sent in english:
			f_sent = f_line.strip()
			length_diff = abs(len(e_sent.split(" ")) - len(f_sent.split(" ")))
			result.write(e_sent + " ||| " + f_sent)
			result.write(" ||| " + str(length_diff) + "\n")
		f_line = f_sentences.readline()
	f_line = f_sentences.readline()

result.close()



