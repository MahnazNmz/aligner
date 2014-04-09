import optparse

optparser = optparse.OptionParser()
optparser.add_option("-e", "--english_pairs", dest="english_pairs", default="data/pairs.enu.dev", help="english pairs")
optparser.add_option("-f", "--foreign_pairs", dest="foreign_pairs", default="data/pairs.esn.dev", help="foreign pairs")
optparser.add_option("-o", "--one_grams", dest="one_grams", default="data1_grams", help="one gram tanslation table")
optparser.add_option("-t", "--two_grams", dest="two_grams", default="data/2_grams", help="two gram translation table")
(opts, args) = optparser.parse_args()

result = open("pairs_withFeatures.txt", "w")

onegram_file = open(opts.one_grams, "r")

one_grams_f_e = {}
for line in onegram_file:
	f, e, feats = (l.strip() for l in line.split("|||"))
	prob, _, _, _ = (float(n.strip()) for n in feats.split(" "))
	#the value at one_grams_f_e[f] for each f is a mapping from the english translation
	#to its probability
	if f not in one_grams_f_e:
		one_grams_f_e[f] = {}
	one_grams_f_e[f][e] = prob


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
			e_words = e_sent.split(" ")
			f_words = f_sent.split(" ")
			#find difference in sentence length
			length_diff = abs(len(e_words) - len(f_words))
			#find num of spanish translation found in english
			totalProb = 0
			for f_w in f_words:
				if f_w in one_grams_f_e:
					#find english translations of f_w that are present in the english sentences
					matches = (set(one_grams_f_e[f_w].keys()) & set(e_words))
					if len(matches) > 0:
						#add the probability from the best match
						totalProb += max([one_grams_f_e[f_w][e] for e in matches])
			translationScore = float(totalProb) / len(f_words)
			result.write(e_sent + " ||| " + f_sent)
			result.write(" ||| " + str(length_diff) + " " + str(translationScore) + "\n")
		f_line = f_sentences.readline()
	f_line = f_sentences.readline()

result.close()



