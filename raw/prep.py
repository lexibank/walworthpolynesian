from lingpy import *
from lingpy.compare.partial import Partial

def run(wordlist):
    D = {0: [c for c in wordlist.columns]+["alignment", "cogids"]}
    part = Partial(wordlist)
    #part.get_partial_scorer(runs=100)
    part.partial_cluster(method="sca", threshold=0.45, ref="cogids")
    alms = Alignments(part, ref="cogids")
    alms.align()
    for idx in alms:
        if not alms[idx, 'note']:
            alms[idx, 'note'] = ''
    for idx in part:
        D[idx] = [alms[idx, h] for h in D[0]]
    return D
