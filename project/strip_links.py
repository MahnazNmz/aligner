import re

en = open("rendered.esn.dev", "r")

for line in en:
	links = re.findall(r'\[[^\]]*\]', line)
	print " ".join(links)