import optparse

optparser = optparse.OptionParser()
optparser.add_option("-e", "--english_pairs", dest="english_pairs", default="data/orig.enu.dev", help="english pairs")
optparser.add_option("-f", "--foreign_pairs", dest="foreign_pairs", default="data/orig.esn.dev", help="foreign pairs")
optparser.add_option("-o", "--one_grams", dest="one_grams", default="data/pruned_1_grams", help="one gram tanslation table")
optparser.add_option("-t", "--two_grams", dest="two_grams", default="data/pruned_2_grams", help="two gram translation table")
optparser.add_option("-r", "--result", dest="result_name", default="pairs_withFeatures.dev", help="name of file to write to")
(opts, args) = optparser.parse_args()

result = open(opts.result_name, "w")

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

twogram_file = open(opts.two_grams, "r")

two_grams_f_e = {}
for line in twogram_file:
	f, e, feats = (l.strip() for l in line.split("|||"))
	prob, _, _, _ = (float(n.strip()) for n in feats.split(" "))
	#the value at two_grams_f_e[f] for each f is a mapping from the english translation
	#to its probability
	if f not in two_grams_f_e:
		two_grams_f_e[f.strip()] = {}
	two_grams_f_e[f.strip()][e.strip()] = prob


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
			e_words = [e.lower() for e in e_sent.split(" ")]
			f_words = [f.lower() for f in f_sent.split(" ")]
			#find difference in sentence length
			length_diff = abs(len(e_words) - len(f_words))
			#find num of spanish translation found in english
			totalProb_onegram = 0
			for f_w in f_words:
				#same word occurs in both sentences (i.e. names, places, cognates)
				if f_w.lower() in e_words:
					totalProb_onegram += 1
					continue
				if f_w.lower() in one_grams_f_e:
					#find english translations of f_w that are present in the english sentences
					matches = (set(one_grams_f_e[f_w.lower()].keys()) & set(e_words))
					if len(matches) > 0:
						#add the probability from the best match
						totalProb_onegram += max([one_grams_f_e[f_w.lower()][e] for e in matches])
			onegram_Score_f = float(totalProb_onegram) / (len(f_words))
			onegram_Score_e = float(totalProb_onegram) / (len(e_words))

			twogram_Score_e = 0
			twogram_Score_f = 0
			if len(f_words) >= 2:
				#make set of two grams in english sentence
				#get two gram probability score
				totalProb_twogram = 0
				for index_start in range(0, len(f_words) - 1):
					index_end = index_start + 2
					two_gram = " ".join(f_words[index_start:index_end])
					if two_gram in e_sent:
						totalProb_twogram += 1
						continue
					if two_gram.lower() in two_grams_f_e:
						matches = (set(two_grams_f_e[two_gram.lower()].keys()) & set(e_words))
						if(len(matches) > 0):
							totalProb_twogram += max([two_grams_f_e[two_gram.lower()][e] for e in matches])
				twogram_Score_f = float(totalProb_twogram) / len(f_words)
				twogram_Score_e = float(totalProb_twogram) / len(e_words)
			result.write(e_sent + " ||| " + f_sent)
			result.write(" ||| " + str(length_diff) + " " + str(onegram_Score_e) + " " + str(onegram_Score_f) + " " + str(twogram_Score_e) + " "  + str(twogram_Score_f) + "\n")

		f_line = f_sentences.readline()
	f_line = f_sentences.readline()

result.close()



