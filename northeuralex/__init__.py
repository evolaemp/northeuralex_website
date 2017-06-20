from pyramid.config import Configurator

from clld.interfaces import IMapMarker
from clld.web.icon import ICON_MAP


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
Dictionary mapping language families to clld.web.icon.Icon instances. Used in
the get_map_marker hook.
"""
FAMILY_ICONS = {
    'Uralic': ICON_MAP['s009900'],
    'Indo-European': ICON_MAP['fdd0000'],
    'Turkic': ICON_MAP['c0000dd'],
    'Mongolic': ICON_MAP['c00ff00'],
    'Tungusic': ICON_MAP['t00ffff'],
    'Dravidian': ICON_MAP['c990099'],
    'Nakh-Daghestanian': ICON_MAP['cffff00'],
    '_default': ICON_MAP['cff6600'] }



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
    family = None

    if isinstance(item, models.Doculect):
        family = item.family
    elif isinstance(item, models.Synset):
        family = item.language.family

    if family not in FAMILY_ICONS:
        family = '_default'

    return FAMILY_ICONS[family].url(req)



def main(global_config, **settings):
    """
    Returns a Pyramid WSGI application. Apart from the clld boilerplate, it
    orders the home sub-navigation and registers the get_map_marker hook.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.registry.settings['home_comp'] = ['help', 'download', 'legal', 'contact']

    config.registry.registerUtility(get_map_marker, IMapMarker)

    return config.make_wsgi_app()
