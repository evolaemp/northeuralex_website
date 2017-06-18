import collections
import csv

from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from clld.scripts.util import bibtex2source, initializedb

from northeuralex.models import Concept, Doculect, Synset, Word



"""
Dataset classes
"""

class LangDataset:
    """
    Handles reading the NorthEuraLex' language data dataset.
    """

    class LangDatasetDialect(csv.Dialect):
        """
        Describes the tsv dialect used for the language data file.
        """
        delimiter = '\t'
        lineterminator = '\r\n'
        quoting = csv.QUOTE_NONE
        strict = True


    Language = collections.namedtuple('Language', [
        'name', 'iso_code', 'glotto_code',
        'family', 'subfamily', 'latitude', 'longitude'])


    def __init__(self, dataset_fp):
        """
        Constructor.
        """
        self.dataset_fp = dataset_fp


    def gen_langs(self):
        """
        Yields a Language named tuple at a time.
        """
        with open(self.dataset_fp, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, dialect=self.LangDatasetDialect)
            for row in reader:
                yield self.Language(row['name'],
                        row['iso_code'], row['glotto_code'],
                        row['family'], row['subfamily'],
                        row['latitude'], row['longitude'])



class ConceptDataset:
    """
    Handles reading the NorthEuraLex' concept dataset.
    """

    class ConceptDatasetDialect(csv.Dialect):
        """
        Describes the tsv dialect used for the concepts data file.
        """
        delimiter = '\t'
        lineterminator = '\r\n'
        quoting = csv.QUOTE_NONE
        strict = True


    Concept = collections.namedtuple('Concept', [
        'id',  # the NorthEuraLex ID
        'name',  # the proposed Concepticon, without the underscores
        'german',  # the German gloss + annotation
        'english',  # the English gloss + annotation
        'russian',  # the Russian gloss + annotation
        'concepticon_id', 'concepticon_name'])


    @staticmethod
    def extract_german(concept_id):
        """
        NorthEuraLex concept IDs are strings of the form GERMAN_WORD::POS. This
        static method extracts the German word from the concept ID.
        """
        parts = concept_id.split('::')
        assert len(parts) == 2
        return parts[0]


    @staticmethod
    def make_gloss_field(gloss, annotation):
        """
        The Concept's fields german, english, and russian are composed of the
        respective language's gloss and annotation.
        """
        if annotation and annotation != '[]':
            return '{} {}'.format(gloss, annotation)
        else:
            return gloss


    def __init__(self, dataset_fp):
        """
        Constructor.
        """
        self.dataset_fp = dataset_fp


    def gen_concepts(self):
        """
        Yields a Concept named tuple at a time.
        """
        with open(self.dataset_fp, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, dialect=self.ConceptDatasetDialect)
            for line in reader:
                yield self.Concept(
                        line['id_nelex'],
                        line['concepticon_proposed'].replace('_', ' '),
                        self.make_gloss_field(self.extract_german(line['id_nelex']),
                                line['annotation_de']),
                        self.make_gloss_field(line['gloss_en'], line['annotation_en']),
                        self.make_gloss_field(line['gloss_ru'], line['annotation_ru']),
                        int(line['concepticon_id']),
                        line['concepticon'])



class MainDataset:
    """
    Handles reading the main NorthEuraLex dataset.
    """

    class MainDatasetDialect(csv.Dialect):
        """
        Describes the tsv dialect used for the dataset file.
        """
        delimiter = '\t'
        lineterminator = '\r\n'
        quoting = csv.QUOTE_NONE
        strict = True


    Word = collections.namedtuple('Word', [
        'iso_code', 'glotto_code', 'concept',
        'form', 'raw_ipa', 'norm_ipa', 'next_step'])


    @staticmethod
    def normalise_ipa(ipa):
        """
        NorthEuraLex dataset files conform to the CLDF format which requires
        IPA transcriptions to comprise interval-separated tokens. This static
        method collapses the extra whitespace producing canonical IPA.
        """
        return ipa.replace(' ', '')


    def __init__(self, dataset_fp):
        """
        Constructor.
        """
        self.dataset_fp = dataset_fp


    def gen_words(self):
        """
        Yields a Word named tuple at a time.
        """
        with open(self.dataset_fp, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, dialect=self.MainDatasetDialect)
            for line in reader:
                yield self.Word(line['Language_ID'],
                            line['Glottocode'],
                            line['Concept_ID'],
                            line['Word_Form'],
                            line['rawIPA'],
                            self.normalise_ipa(line['IPA']),
                            line['Next_Step'])



"""
Database-populating functions
"""

def add_meta_data(session):
    """
    Creates and adds to the given SQLAlchemy session the common.Dataset and
    related model instances that comprise the project's meta info.

    Helper for the main function that keeps the meta data in one place for
    easier reference and editing.
    """
    dataset = common.Dataset(id='northeuralex',
            name='NorthEuraLex',
            description='Lexicostatistical Database of Northern Eurasia',
            publisher_name='Johannes Dellert',
            publisher_place='Tübingen',
            publisher_url='http://www.sfs.uni-tuebingen.de/~jdellert/',
            license='https://creativecommons.org/licenses/by-sa/4.0/',
            jsondata={
                'license_icon': 'cc-by-sa.png',
                'license_name': 'Creative Commons Attribution-ShareAlike 4.0 International License'},
            contact='',
            domain='northeuralex.org')
    session.add(dataset)

    dataset.editors.append(common.Editor(
        contributor=common.Contributor(id='jdellert', name='Johannes Dellert')))



def add_sources(sources_file_path, session):
    """
    Creates and adds to the given SQLAlchemy session the common.Source model
    instances that comprise the project's references. Expects the path to a
    bibtex file as its first argument.

    Helper for the main function.
    """
    bibtex_db = bibtex.Database.from_file(sources_file_path, encoding='utf-8')

    for record in bibtex_db:
        session.add(bibtex2source(record))



def add_concepts(concepts_dataset, session):
    """
    Creates and adds to the given SQLAlchemy session the Concept instances
    harvested from the given ConceptDataset instance. Returns a dict of the
    added model instances with the NorthEuraLex concept IDs being the keys.

    Helper for the main function.
    """
    d = {}

    for index, concept in enumerate(concepts_dataset.gen_concepts(), 1):
        d[concept.id] = Concept(id=index,
                name=concept.name,
                english_name=concept.english,
                german_name=concept.german,
                russian_name=concept.russian,
                concepticon_id=concept.concepticon_id,
                concepticon_name=concept.concepticon_name)
        session.add(d[concept.id])

    return d



def add_doculects(lang_dataset, session):
    """
    Creates and adds to the given SQLAlchemy session the Doculect instances
    harvested from the given LangDataset instance. Returns a dict of the added
    model instances with the respective ISO codes being the keys.

    Helper for the main function.
    """
    d = {}

    for lang in lang_dataset.gen_langs():
        d[lang.iso_code] = Doculect(id=lang.iso_code,
                name=lang.name,
                iso_code=lang.iso_code,
                glotto_code=lang.glotto_code,
                family=lang.family,
                subfamily=lang.subfamily,
                latitude=lang.latitude,
                longitude=lang.longitude)
        session.add(d[lang.iso_code])

    return d



def main(args):
    """
    Populates the database. Expects: (1) the db to be empty; (2) the main_data,
    lang_data, concept_data, and sources_data args to be present in the given
    argparse.Namespace instance.

    This function is called within a db transaction, the latter being handled
    by initializedb.
    """
    main_dataset = MainDataset(args.main_data)

    add_meta_data(DBSession)
    add_sources(args.sources_data, DBSession)

    concepts = add_concepts(ConceptDataset(args.concept_data), DBSession)
    doculects = add_doculects(LangDataset(args.lang_data), DBSession)

    last_synset = None

    for word in main_dataset.gen_words():
        assert word.concept in concepts
        assert word.iso_code in doculects
        assert word.glotto_code == doculects[word.iso_code].glotto_code

        if last_synset is None \
        or last_synset.language != doculects[word.iso_code] \
        or last_synset.parameter != concepts[word.concept]:
            last_synset = Synset(id='{}-{}'.format(word.iso_code, word.concept),
                    language=doculects[word.iso_code],
                    parameter=concepts[word.concept])
            DBSession.add(last_synset)

        DBSession.add(Word(id='{}-{}-{}'.format(word.iso_code, word.concept, word.form),
                valueset=last_synset,
                name=word.form,
                raw_ipa=word.raw_ipa,
                norm_ipa=word.norm_ipa,
                next_step=word.next_step))



"""
The cli

The clld.scripts.util.initializedb func is a wrapper around the main func, but
it uses its own argparse.ArgumentParser instance. Thus, there are two ways to
avoid hardcoding the paths to the NorthEuraLex datasets: (1) init an
ArgumentParser instance here and fake some sys.argv input to the initializedb's
instance so that initializedb does not break; (2) add new arguments to
initializedb's instance in the undocumented and weird way that seems to have
been provided for such cases. The latter option is implemented.
"""
if __name__ == '__main__':
    main_data_arg = [('main_data',), {
        'help': 'path to the csv file that contains the northeuralex data'}]
    lang_data_arg = [('lang_data',), {
        'help': 'path to the tsv file that contains the language data'}]
    concept_data_arg = [('concept_data',), {
        'help': 'path to the tsv file that contains the concept data'}]
    sources_data_arg = [('sources_data',), {
        'help': 'path to the bibtex file that contains the references'}]

    initializedb(main_data_arg, lang_data_arg, concept_data_arg,
            sources_data_arg, create=main)
