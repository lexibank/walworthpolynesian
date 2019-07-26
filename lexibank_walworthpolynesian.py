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
            for name, gcode in set([(b, c) for (a, b, c) in wl.iter_rows('doculect',
                'glottocode')]):
                ds.add_language(ID=slug(name), Name=name, Glottocode=gcode)
            for idx in pb(wl, desc='cldfify'):
                ds.add_lexemes(
                        Language_ID=slug(wl[idx, 'doculect']),
                        Parameter_ID={'1433': '353', '602': '2486'}.get(
                            wl[idx, 'concepticon_id'],
                            wl[idx, 'concepticon_id']),
                        Value = wl[idx, 'value'],
                        Form = wl[idx, 'form'],
                        Segments={1510: "f e i + s a ŋ a".split(), 2010: "ʔ a k a + k i u + k i u".split(), 5907: "ʔ a + ʔ a n o".split(), 7247: "f e + f e l o".split()}.get(idx) or wl[idx, 'segments'],
                        Source = [wl[idx, 'source']]
                        )
