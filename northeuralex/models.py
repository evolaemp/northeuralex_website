from clld.db.meta import CustomModelMixin
from clld.db.models.common import Language, Parameter, ValueSet, Value
from clld import interfaces

from sqlalchemy import Column, ForeignKey, Integer, Unicode

from zope.interface import implementer



@implementer(interfaces.ILanguage)
class Doculect(CustomModelMixin, Language):
    """
    From Language this model inherits: latitude (float), longitude (float).
    """
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    iso_code = Column(Unicode)
    glotto_code = Column(Unicode)



@implementer(interfaces.IParameter)
class Concept(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)



@implementer(interfaces.IValueSet)
class Synset(CustomModelMixin, ValueSet):
    pk = Column(Integer, ForeignKey('valueset.pk'), primary_key=True)



@implementer(interfaces.IValue)
class Word(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    ipa = Column(Unicode)
