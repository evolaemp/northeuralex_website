from clld.db.meta import DBSession
from clld.db.models import common
from clld.scripts.util import initializedb, Data



def main(args):
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
