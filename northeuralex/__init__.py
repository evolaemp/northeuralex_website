from pyramid.config import Configurator

from clld.db.meta import DBSession
from clld.interfaces import IMapMarker
from clld.web.icon import ORDERED_ICONS


"""
Even if not used, these models should still be imported. The original comment:
we must make sure custom models are known at database initialization!
"""
from northeuralex import models



"""
An ugly hack to register the following strings for i10n/l18n so that the model
names change in the templates. Ugh!

This is how the problem of renaming the models is handled in other clld apps
(e.g. asjp and wals) as well.
"""
_ = lambda x: x
_('Parameter')
_('Parameters')



"""
Dictionary mapping language families to clld.web.icon.Icon instances. Inited in
the main function and used in the get_map_marker hook.
"""
FAMILY_ICONS = {}



def get_map_marker(item, req):
    """
    Hook called for each marker on each map. Determines the map marker for the
    given item (the latter would be an instance of a different class depending
    on the map). Returns the URL of the selected map marker.

    In other words, makes sure that each marker on a map would consistently use
    the same icon depending on the language family.

    The idea how to achieve different markers for different language families
    was stolen from the __init__ module of the sails clld project.
    """
    if isinstance(item, models.Doculect):
        family = item.family
    elif isinstance(item, models.Synset):
        family = item.language.family
    else:
        return ''

    return FAMILY_ICONS[family].url(req)



def main(global_config, **settings):
    """
    Returns a Pyramid WSGI application. Apart from the clld boilerplate, it
    orders the home sub-navigation, inits the FAMILY_ICONS dict and registers
    the get_map_marker hook.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.registry.settings['home_comp'] = ['help', 'download', 'legal', 'contact']

    family_query = DBSession.query(models.Doculect.family).distinct()
    family_query = map(lambda x: x[0], family_query)
    for family in family_query:
        FAMILY_ICONS[family] = ORDERED_ICONS[len(FAMILY_ICONS)]

    config.registry.registerUtility(get_map_marker, IMapMarker)

    return config.make_wsgi_app()
