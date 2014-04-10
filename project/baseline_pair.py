import os

#format development data
os.system("python make_pairsWithFeatures.py -r pairs_withFeatures.dev")
#format test data
os.system("python make_pairsWithFeatures.py -e test/orig.enu.test -f test/orig.esn.test -r pairs_withFeatures.test")
#learn weights for features and use them to generate pairs for test
os.system("python learn_weights.py -n pairs_withFeatures.dev | python generate_pairs.py -w -")