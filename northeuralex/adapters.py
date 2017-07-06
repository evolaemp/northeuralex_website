from clld.web.adapters import excel
from clld import interfaces



class ExcelLanguages(excel.ExcelAdapter):

    def header(self, ctx, req):
        return ['name', 'glotto_code', 'iso_code',
                'family', 'subfamily', 'latitude', 'longitude']

    def row(self, ctx, req, doculect):
        return [doculect.name, doculect.glotto_code, doculect.iso_code,
                doculect.family, doculect.subfamily,
                '{:.2f}'.format(doculect.latitude),
                '{:.2f}'.format(doculect.longitude)]



class ExcelConcepts(excel.ExcelAdapter):

    def header(self, ctx, req):
        return ['id', 'name', 'english', 'german', 'russian',
                'concepticon_id', 'concepticon_name']

    def row(self, ctx, req, concept):
        return [concept.id, concept.name,
                concept.english_name, concept.german_name, concept.russian_name,
                concept.concepticon_id, concept.concepticon_name]



class ExcelWords(excel.ExcelAdapter):

    def header(self, ctx, req):
        return ['lang_iso_code', 'concept_id',
                'ortho_form', 'raw_ipa', 'next_step']

    def row(self, ctx, req, word):
        return [word.valueset.language.iso_code,
                word.valueset.parameter.id,
                word.name, word.raw_ipa, word.next_step]



def includeme(config):
    config.register_adapter(ExcelLanguages, interfaces.ILanguage)
    config.register_adapter(ExcelConcepts, interfaces.IParameter)
    config.register_adapter(ExcelWords, interfaces.IValue)
