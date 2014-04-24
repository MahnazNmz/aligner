import re
import wikipydia
import optparse
import urllib 

optparser = optparse.OptionParser()
optparser.add_option("-l", "--language", dest="language", default="en", help="language of articles to look for")
(opts, args) = optparser.parse_args()

filename = ""
if opts.language == "en":
	filename = "rendered.enu.dev"
elif opts.language == "es":
	filename = "rendered.esn.dev"

f = open(filename, "r")

for line in f:
	links = re.findall(r'\[[^\]]*\]', line)
	for (i, l) in enumerate(links):
		l = l.strip("[]")
		l = l.replace(" ","")
		l = l.replace("-LRB-","(")
		l = l.replace("-RRB-",")")
		l = urllib.unquote(l).decode('utf8')
		links[i] = l

	toRemove = []
	for (i,l) in enumerate(links):
		if opts.language == "en":
			if "File" in l:
				toRemove.append(i)
			if "Wikipedia" in l:
				toRemove.append(i)
			if "edit" in l:
				toRemove.append(i)
			if "Special:" in l:
				toRemove.append(i)
			if "a,b" in l:
				toRemove.append(i)
			if l == "originallypublishedin1973":
				toRemove.append(i)
		if opts.language == "es":
			if "Archivo" in l:
				toRemove.append(i)
			if "Wikipedia" in l:
				toRemove.append(i)
			if l == "editar":
				toRemove.append(i)

	for i in sorted(toRemove, reverse=True):
		if i < len(links):
			del links[i]

	if opts.language == "en":
		for (i, link) in enumerate(links):
			allLanguages = wikipydia.query_language_links(link)
			if "es" in allLanguages:
				links[i] = allLanguages['es']
				links[i] = links[i].replace(" ","_")
		print u" ".join([urllib.quote(l.encode('utf-8')) for l in links])
	else:
		print u" ".join([urllib.quote(l.encode('utf-8')) for l in links])