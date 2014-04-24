orig = open("data/orig.enu.dev", "r")
rendered = open("rendered.enu.dev", "r")

for (o,r) in zip(orig, rendered):
	print o + " ||| " + r