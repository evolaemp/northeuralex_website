import collections
import csv

from clld.db.meta import DBSession
from clld.db.models import common
from clld.scripts.util import initializedb

from northeuralex.models import Concept, Doculect, Synset, Word



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
        'iso_code', 'glotto_code', 'latitude', 'longitude', 'name'])


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
            reader = csv.reader(f, dialect=self.LangDatasetDialect)
            for row in reader:
                yield self.Language._make(row)



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
        'iso_code', 'glotto_code', 'concept', 'form', 'ipa'])


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
                yield self.Word(line['Language_ID'], line['Glottocode'],
                            line['Concept_ID'], line['Word_Form'], line['rawIPA'])



def init_meta_data(session):
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



def main(args):
    """
    Populates the database. Expects: (1) the db to be empty; (2) main_data and
    lang_data to be present in the args argparse.Namespace instance.

    This function is called within a db transaction, the latter being handled
    by initializedb.
    """
    main_dataset = MainDataset(args.main_data)
    lang_dataset = LangDataset(args.lang_data)

    all_langs = {}  # iso_code: named tuple
    for lang in lang_dataset.gen_langs():
        all_langs[lang.iso_code] = lang

    init_meta_data(DBSession)

    doculects = {}  # iso_code: model instance
    concepts = {}  # concept: model instance
    last_synset = None

    for word in main_dataset.gen_words():
        if word.concept not in concepts:
            concepts[word.concept] = Concept(id=word.concept, name=word.concept)
            DBSession.add(concepts[word.concept])

        if word.iso_code not in doculects:
            if word.iso_code not in all_langs:
                continue
            doculects[word.iso_code] = Doculect(id=word.iso_code,
                    name=all_langs[word.iso_code].name,
                    iso_code=word.iso_code,
                    glotto_code=word.glotto_code,
                    latitude=all_langs[word.iso_code].latitude,
                    longitude=all_langs[word.iso_code].longitude)
            DBSession.add(doculects[word.iso_code])

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
                ipa=word.ipa))



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

    initializedb(main_data_arg, lang_data_arg, create=main)
