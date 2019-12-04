import pathlib

from pylexibank import Dataset as BaseDataset
from pylexibank import FormSpec
from lingpy import *
from pylexibank.util import progressbar

def to_boolean(x):
    return x.lower() == 'true'
        


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "walworthpolynesian"
    form_spec = FormSpec(first_form_only=True)

    def cmd_makecldf(self, args):
        wl = Wordlist(str(self.raw_dir / 'polynesian-aligned_22112018.tsv'))
        args.writer.add_sources(*self.raw_dir.read_bib())
        for c in self.conceptlists[0].concepts.values():
            args.writer.add_concept(
                ID=c.concepticon_id,
                Name=c.english,
                Concepticon_ID=c.concepticon_id,
                Concepticon_Gloss=c.concepticon_gloss)
        
        lm = {l['Name']: l['ID'] for l in self.languages}
        args.writer.add_languages()
        
        for idx in progressbar(wl, desc='cldfify'):
            if [x for x in wl[idx, 'segments'] if x in ['+s', 'u+', '+ʔ', 'e+']]:
                segments = []
                for segment in wl[idx, 'segments']:
                    if '+' in segment and len(segment) > 1:
                        segments += list(segment)
                    else:
                        segments += [segment]
                wl[idx, 'segments'] = segments

            lex = args.writer.add_form_with_segments(
                Language_ID=lm[wl[idx, 'doculect']],
                Parameter_ID={'1433': '353', '602': '2486'}.get(
                    wl[idx, 'concepticon_id'], wl[idx, 'concepticon_id']),
                Value=wl[idx, 'value'],
                Form=wl[idx, 'form'],
                Segments={
                    1510: "f e i + s a ŋ a".split(),
                    2010: "ʔ a k a + k i u + k i u".split(),
                    5907: "ʔ a + ʔ a n o".split(),
                    7247: "f e + f e l o".split(),
                }.get(idx) or wl[idx, 'segments'],
                Source=[wl[idx, 'source']],
                Cognacy=wl[idx, 'cogid'],
                Loan=to_boolean(wl[idx, 'loan']),
                Comment=wl[idx, 'comment']
            )

            args.writer.add_cognate(
                lexeme=lex,
                Source=['walworth_mary_2018_1689909'],
                Cognateset_ID=wl[idx, 'cogid']
            )
