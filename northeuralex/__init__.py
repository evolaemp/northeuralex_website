from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from northeuralex import models


"""
An ugly hack to register the following strings for i10n/l18n so that the model
names change in the templates. Ugh!

This is how the problem of renaming the models is handled in other clld apps
(e.g. asjp and wals) as well.
"""
_ = lambda x: x
_('Language')
_('Languages')
_('Parameter')
_('Parameters')



def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')
    return config.make_wsgi_app()
