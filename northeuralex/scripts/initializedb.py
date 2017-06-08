import collections
import csv

from clld.db.meta import DBSession
from clld.db.models import common
from clld.scripts.util import initializedb, Data



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



def main(cls, args):
    """
    Populates the database. Expects: (1) the db to be empty; (2) main_data and
    lang_data to be present in the args argparse.Namespace instance.

    This function is called within a db transaction, the latter being handled
    by initializedb.
    """
    data = Data()

    dataset = common.Dataset(id='northeuralex', domain='northeuralex.clld.org')
    DBSession.add(dataset)



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
