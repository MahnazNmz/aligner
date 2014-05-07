orig = open("test/pairs.enu.test", "r")
rendered = open("test/pairs.esn.test", "r")

for (o,r) in zip(orig, rendered):
	print o.strip() + " ||| " + r.strip()
