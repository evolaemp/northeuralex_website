import json

from clld.web.adapters import csv, excel, JsonIndex
from clld import interfaces

from clldutils.dsv import UnicodeWriter



"""
Mixin classes

Each of these includes two methods: header and row. The former is invoked once
per download while the latter is called once for each model instance. The idea
is taken from clld.web.adapters.excel.
"""

class LanguagesMixin:

    def header(self, ctx, req):
        return ['name', 'glotto_code', 'iso_code',
                'family', 'subfamily', 'latitude', 'longitude']

    def row(self, ctx, req, doculect):
        return [doculect.name, doculect.glotto_code, doculect.iso_code,
                doculect.family, doculect.subfamily,
                '{:.2f}'.format(doculect.latitude),
                '{:.2f}'.format(doculect.longitude)]



class ConceptsMixin:

    def header(self, ctx, req):
        return ['id', 'name', 'english', 'german', 'russian',
                'concepticon_id', 'concepticon_name']

    def row(self, ctx, req, concept):
        return [concept.id, concept.name,
                concept.english_name, concept.german_name, concept.russian_name,
                concept.concepticon_id, concept.concepticon_name]



class WordsMixin:

    def header(self, ctx, req):
        return ['lang_iso_code', 'concept_id',
                'ortho_form', 'raw_ipa', 'next_step']

    def row(self, ctx, req, word):
        return [word.valueset.language.iso_code,
                word.valueset.parameter.id,
                word.name, word.raw_ipa, word.next_step]



"""
excel adapters
"""

class LanguagesExcelAdapter(LanguagesMixin, excel.ExcelAdapter):
    pass


class ConceptsExcelAdapter(ConceptsMixin, excel.ExcelAdapter):
    pass


class WordsExcelAdapter(WordsMixin, excel.ExcelAdapter):
    pass



"""
csv adapters

The base csv adapter overwrites clld's one in order to replace item.csv_head
and item.to_csv calls with calls to the mixins defined above. In other words,
it applies the logic of clld's base excel adapter.
"""

class CsvAdapter(csv.CsvAdapter):

    def render(self, ctx, req):
        with UnicodeWriter() as writer:
            writer.writerow(self.header(ctx, req))

            for item in ctx.get_query(limit=csv.QUERY_LIMIT):
                writer.writerow(self.row(ctx, req, item))

            return writer.read()



class LanguagesCsvAdapter(LanguagesMixin, CsvAdapter):
    pass


class ConceptsCsvAdapter(ConceptsMixin, CsvAdapter):
    pass


class WordsCsvAdapter(WordsMixin, CsvAdapter):
    pass



"""
json adapters

The base json adapter replaces the default JsonIndex and applies the logic of
clld's base excel adapter.
"""

class JsonAdapter(JsonIndex):

    def render(self, ctx, req):
        rows = []

        header = self.header(ctx, req)

        for item in ctx.get_query(limit=csv.QUERY_LIMIT):
            rows.append({key: value
                for key, value in zip(header, self.row(ctx, req, item))})

        return json.dumps({'rows': rows}, ensure_ascii=False)



class LanguagesJsonAdapter(LanguagesMixin, JsonAdapter):
    pass


class ConceptsJsonAdapter(ConceptsMixin, JsonAdapter):
    pass


class WordsJsonAdapter(WordsMixin, JsonAdapter):
    pass



"""
Hooks
"""

def includeme(config):
    """
    Magical (not in the good sense) hook that replaces the default download
    adapters with the custom ones defined in this module.
    """
    config.register_adapter(LanguagesCsvAdapter, interfaces.ILanguage)
    config.register_adapter(ConceptsCsvAdapter, interfaces.IParameter)
    config.register_adapter(WordsCsvAdapter, interfaces.IValue)

    config.register_adapter(LanguagesExcelAdapter, interfaces.ILanguage)
    config.register_adapter(ConceptsExcelAdapter, interfaces.IParameter)
    config.register_adapter(WordsExcelAdapter, interfaces.IValue)

    config.register_adapter(LanguagesJsonAdapter, interfaces.ILanguage)
    config.register_adapter(ConceptsJsonAdapter, interfaces.IParameter)
    config.register_adapter(WordsJsonAdapter, interfaces.IValue)
