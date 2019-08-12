from clldutils.path import Path
from pylexibank.dataset import NonSplittingDataset as BaseDataset
from lingpy import *
from pylexibank.util import pb
from clldutils.misc import slug


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "walworthpolynesian"

    def cmd_install(self, **kw):
        """
        Convert the raw data to a CLDF dataset.

        Use the methods of `pylexibank.cldf.Dataset` after instantiating one as context:

        """
        wl = Wordlist(self.dir.joinpath('raw', 'polynesian-aligned_22112018.tsv').as_posix())
        with self.cldf as ds:
            ds.add_sources(*self.raw.read_bib())
            for c in self.conceptlist.concepts.values():
                ds.add_concept(ID=c.concepticon_id, Name=c.english,
                        Concepticon_ID=c.concepticon_id,
                        Concepticon_Gloss=c.concepticon_gloss)
            lm = {l['Name']: l['ID'] for l in self.languages}
            ds.add_languages()
            for idx in pb(wl, desc='cldfify'):
                if [x for x in wl[idx, 'segments'] if x in ['+s', 'u+', '+ʔ',
                    'e+']]:
                    segments = []
                    for segment in wl[idx, 'segments']:
                        if '+' in segment and len(segment) > 1:
                            segments += list(segment)
                        else:
                            segments += [segment]
                    wl[idx, 'segments'] = segments


                ds.add_segments(
                        Language_ID=lm[wl[idx, 'doculect']],
                        Parameter_ID={'1433': '353', '602': '2486'}.get(
                            wl[idx, 'concepticon_id'],
                            wl[idx, 'concepticon_id']),
                        Value = wl[idx, 'value'],
                        Form = wl[idx, 'form'],
                        Segments = wl[idx, 'segments'],
                        Source = [wl[idx, 'source']]
                        )
