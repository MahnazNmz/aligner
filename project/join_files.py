orig = open("data/orig.esn.dev", "r")
rendered = open("rendered.esn.dev", "r")

for (o,r) in zip(orig, rendered):
	print o + " ||| " + r