from clld.db.meta import DBSession
from clld.web.datatables.base import Col, IntegerIdCol, LinkToMapCol, LinkCol
from clld.web.util.helpers import external_link, link
from clld.web import datatables

from northeuralex.models import Concept, Doculect, Word



"""
Columns
"""

class IsoCodeCol(Col):
    """
    Custom column to set a proper title for the iso_code column of the
    languages table.
    """

    __kw__ = {'sTitle': 'ISO 639-3'}



class GlottoCodeCol(Col):
    """
    Custom column to present the glotto_code column of the languages table as a
    link to the respective languoid in Glottolog.
    """

    __kw__ = {'sTitle': 'Glottocode'}

    def format(self, doculect):
        href = 'http://glottolog.org/resource/languoid/id/{}'.format(doculect.glotto_code)
        return external_link(href, doculect.glotto_code)



class FamilyCol(Col):
    """
    Custom column to replace the search with a drop-down for the family column
    of the languages table.

    Unlike in, e.g., NextStepCol, the choices have to be set in the constructor
    because otherwise the unit tests do not work.
    """

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = sorted([
            x[0] for x in DBSession.query(Doculect.family).distinct()])

        super().__init__(*args, **kwargs)



class SubfamilyCol(Col):
    """
    Custom column to replace the search with a drop-down for the subfamily
    column of the languages table.

    Unlike in, e.g., NextStepCol, the choices have to be set in the constructor
    because otherwise the unit tests do not work.
    """

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = sorted([
            x[0] for x in DBSession.query(Doculect.subfamily).distinct()])

        super().__init__(*args, **kwargs)



class ConcepticonCol(Col):
    """
    Custom column to present the concepticon_name column of the concepts table
    as a link to the respective concept in the Concepticon.
    """

    __kw__ = {'sTitle': 'Concepticon'}

    def format(self, concept):
        if concept.concepticon_id:
            href = 'http://concepticon.clld.org/parameters/{}'.format(concept.concepticon_id)
            return external_link(href, concept.concepticon_name)
        else:
            return ''



class ConceptLinkCol(LinkCol):
    """
    Custom column to present the concept column of the words table as a link
    with a title attribute containing the concept's English name.
    """

    def format(self, item):
        concept = self.get_obj(item)
        if concept:
            return link(self.dt.req, concept, **{'title': concept.english_name})
        else:
            return ''



class DoculectLinkCol(LinkCol):
    """
    Custom column to present the doculect column of the words table as a link
    with a title attribute containing the doculect's family and subfamily.
    """

    def format(self, item):
        doculect = self.get_obj(item)
        if doculect:
            title = '{} ({}, {})'.format(doculect.name,
                        doculect.family, doculect.subfamily)
            return link(self.dt.req, doculect, **{'title': title})
        else:
            return ''



class NextStepCol(Col):
    """
    Custom column to replace the search with a drop-down for the next_step
    column of the words table. Also provides help info in the column's header.
    """

    __kw__ = {
        'sTitle': (
            '<abbr title="'
            'Lorem ipsum dolor sit amet'
            '">Next action</abbr>'),
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
            FamilyCol(self, 'family', model_col=Doculect.family),
            SubfamilyCol(self, 'subfamily', model_col=Doculect.subfamily),
            Col(self, 'latitude'),
            Col(self, 'longitude') ]



class ConceptsDataTable(datatables.Parameters):

    def col_defs(self):
        return [
            IntegerIdCol(self, 'id', model_col=Concept.id),
            LinkCol(self, 'name'),
            Col(self, 'english', model_col=Concept.english_name),
            Col(self, 'german', model_col=Concept.german_name),
            Col(self, 'russian', model_col=Concept.russian_name),
            ConcepticonCol(self, 'concepticon', model_col=Concept.concepticon_name) ]



class WordsDataTable(datatables.Values):

    def col_defs(self):
        res = []

        if self.language:
            res.extend([
                IntegerIdCol(self, 'id', model_col=Concept.id,
                    get_object=lambda x: x.valueset.parameter),
                ConceptLinkCol(self, 'concept', model_col=Concept.name,
                    get_object=lambda x: x.valueset.parameter) ])

        elif self.parameter:
            res.extend([
                DoculectLinkCol(self, 'language', model_col=Doculect.name,
                    get_object=lambda x: x.valueset.language) ])

        res.extend([
            Col(self, 'form', model_col=Word.name, sTitle='Orthographic form'),
            Col(self, 'raw_ipa', model_col=Word.raw_ipa, sTitle='Automatically generated IPA'),
            Col(self, 'norm_ipa', model_col=Word.norm_ipa, sTitle='Normalised IPA'),
            NextStepCol(self, 'next_step', model_col=Word.next_step) ])

        return res



class SourcesDataTable(datatables.Sources):

    def col_defs(self):
        return super().col_defs()[:-1]



"""
Hooks
"""

def includeme(config):
    """
    Magical (not in the good sense) hook that replaces the default data tables
    with the custom ones defined in this module.
    """
    config.register_datatable('languages', LanguagesDataTable)
    config.register_datatable('parameters', ConceptsDataTable)
    config.register_datatable('values', WordsDataTable)
    config.register_datatable('sources', SourcesDataTable)
