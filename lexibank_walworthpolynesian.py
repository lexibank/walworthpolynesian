import pathlib
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import FormSpec
from lingpy import *


def to_boolean(x):
    return x.lower() == 'true'


def fix_segments(inseg):
    # i.e. explode conjoined "+s" etc to "+ s"
    segments = []
    for segment in inseg:
        if '+' in segment and len(segment) > 1:
            segments += list(segment)
        else:
            segments += [segment]
    return segments
    

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "walworthpolynesian"
    
    form_spec = FormSpec(first_form_only=True)

    def cmd_makecldf(self, args):
        args.writer.add_sources(*self.raw_dir.read_bib())
        
        languages = args.writer.add_languages(
            lookup_factory=lambda l: l['Name']
        )
        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english),
            lookup_factory="Name",
        )
        concepts['ash'] = '146_ashes'
        
        
        wl = Wordlist(str(self.raw_dir / 'polynesian-aligned_22112018_corrected.tsv'))
        
        for idx in sorted(wl):
            wl[idx, 'segments'] = fix_segments(wl[idx, 'segments'])
            
            lex = args.writer.add_form_with_segments(
                Language_ID=languages.get(wl[idx, 'doculect']),
                Parameter_ID=concepts.get(wl[idx, 'concept']),
                Value=wl[idx, 'value'],
                Form=wl[idx, 'form'],
                Segments=[{'_': '+'}.get(x, x) for x in wl[idx, 'segments']],
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
