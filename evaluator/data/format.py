import re
import optparse

optparser = optparse.OptionParser()
optparser.add_option("-f", "--file-name", dest="file", default="core-wordnet.txt", help="Name of file to transform")
(opts,_) = optparser.parse_args()
table = dict()
f = [line for line in open(opts.file)]
for line in f:
	 m = re.match("a\ \[.*?\]\ \[(\w+)\]\ (.+)",  line)
	 if m:
	 	syns = [w for w in m.group(2).strip().split(", ") if len(w.split()) == 1]
	 	if len(syns) > 0:
	 		table[m.group(1)] = syns

	 	for syn in syns:
	 		table[syn] = syns + [m.group(1)]
	 		table[syn].remove(syn)
	 		if len(table[syn]) == 0:
	 			table.pop(syn, None)
words = sorted(table.keys())
for w in words:
	print w + ": " + ", ".join(table[w])

	 	

