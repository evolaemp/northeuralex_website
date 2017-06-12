from clld.web.datatables.base import Col, LinkToMapCol, LinkCol
from clld.web.util.helpers import external_link
from clld.web import datatables

from northeuralex.models import Concept, Doculect, Word



"""
Columns
"""

class IsoCodeCol(Col):
    __kw__ = {'sTitle': 'ISO 639-3'}



class GlottoCodeCol(Col):
    __kw__ = {'sTitle': 'Glottocode'}

    def format(self, doculect):
        href = 'http://glottolog.org/resource/languoid/id/{}'.format(doculect.glotto_code)
        return external_link(href, doculect.glotto_code)



class NextStepCol(Col):
    __kw__ = {
        'sTitle': 'Next action',
        'choices': [('validate', 'validate'),
                    ('review', 'review'),
                    ('process', 'process')] }



"""
Tables
"""

class LanguagesDataTable(datatables.Languages):

    def col_defs(self):
        return [
            LinkToMapCol(self, 'm'),
            LinkCol(self, 'name'),
            GlottoCodeCol(self, 'glotto_code', model_col=Doculect.glotto_code),
            IsoCodeCol(self, 'iso_code', model_col=Doculect.iso_code),
            Col(self, 'latitude'),
            Col(self, 'longitude') ]



class ConceptsDataTable(datatables.Parameters):

    def col_defs(self):
        return [
            LinkCol(self, 'name')]



class WordsDataTable(datatables.Values):

    def col_defs(self):
        res = []

        if self.language:
            res.extend([
                LinkCol(self, 'concept', model_col=Concept.name,
                    get_object=lambda x: x.valueset.parameter) ])

        elif self.parameter:
            res.extend([
                LinkCol(self, 'language', model_col=Doculect.name,
                    get_object=lambda x: x.valueset.language) ])

        res.extend([
            Col(self, 'form', model_col=Word.name, sTitle='Orthographic form'),
            Col(self, 'raw_ipa', model_col=Word.raw_ipa, sTitle='Automatically generated IPA'),
            Col(self, 'norm_ipa', model_col=Word.norm_ipa, sTitle='Normalised IPA'),
            NextStepCol(self, 'next_step', model_col=Word.next_step) ])

        return res



def includeme(config):
    """
    Magical (not in the good sense) hook that replaces the default data tables
    with the custom ones defined in this module.
    """
    config.register_datatable('languages', LanguagesDataTable)
    config.register_datatable('parameters', ConceptsDataTable)
    config.register_datatable('values', WordsDataTable)
