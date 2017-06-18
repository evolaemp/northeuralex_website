import os.path
import unittest

from northeuralex.scripts.initializedb import LangDataset, ConceptDataset, MainDataset



FIXTURES_DIR = 'northeuralex/tests/fixtures'



class LangDatasetTestCase(unittest.TestCase):

    def setUp(self):
        self.dataset = LangDataset(os.path.join(FIXTURES_DIR, 'lang_data.tsv'))

    def test_gen_langs(self):
        langs = []
        for lang in self.dataset.gen_langs():
            self.assertTrue(type(lang) is LangDataset.Language)
            langs.append(lang)

        self.assertEqual(len(langs), 107)

        self.assertEqual(langs[0], LangDataset.Language._make([
            'Finnish', 'fin', 'finn1318', 'Uralic', 'Finnic', '61', '24.45']))
        self.assertEqual(langs[-4], LangDataset.Language._make([
            'Chechen', 'che', 'chec1245', 'Nakh-Daghestanian', 'Nakh', '43.5', '45.5']))



class ConceptDatasetTestCase(unittest.TestCase):

    def setUp(self):
        self.dataset = ConceptDataset(os.path.join(FIXTURES_DIR, 'concept_data.tsv'))

    def test_extract_german(self):
        self.assertEqual(self.dataset.extract_german('Auge::N'), 'Auge')
        self.assertEqual(self.dataset.extract_german('Kiefer[Baum]::N'), 'Kiefer[Baum]')

    def test_gen_concepts(self):
        concepts = []

        for concept in self.dataset.gen_concepts():
            self.assertTrue(type(concept) is ConceptDataset.Concept)
            concepts.append(concept)

        self.assertEqual(len(concepts), 48)

        self.assertEqual(concepts[0], ConceptDataset.Concept._make([
            'Auge::N', 'EYE', 'Auge [[Anatomie]]', 'eye [[anatomy]]', 'глаз [[анатомия]]', 1248, 'EYE']))
        self.assertEqual(concepts[17], ConceptDataset.Concept._make([
            'Genick::N', 'NAPE (OF NECK)', 'Genick [hinter Teil des Halses]', 'nape [back side of neck]',
            'затылок [задняя часть головы]', 1347, 'NAPE_(OF_NECK)']))
        self.assertEqual(concepts[47], ConceptDataset.Concept._make([
            'Leber::N', 'LIVER', 'Leber [[Anatomie]]', 'liver [[anatomy]]', 'печень [[анатомия]]', 1224, 'LIVER']))



class MainDatasetTestCase(unittest.TestCase):

    def setUp(self):
        self.dataset = MainDataset(os.path.join(FIXTURES_DIR, 'main_data.tsv'))

    def test_normalise_ipa(self):
        self.assertEqual(self.dataset.normalise_ipa('s i l m æ'), 'silmæ')
        self.assertEqual(self.dataset.normalise_ipa('k æ æ r m ɛ'), 'kæærmɛ')

    def test_gen_words(self):
        words = []
        for word in self.dataset.gen_words():
            self.assertTrue(type(word) is MainDataset.Word)
            self.assertEqual(word.iso_code, 'gle')
            self.assertEqual(word.glotto_code, 'iris1253')
            words.append(word)

        self.assertEqual(len(words), 1278)

        self.assertEqual(words[0], MainDataset.Word._make([
            'gle', 'iris1253', 'Auge::N', 'súil', 'sˠuːlʲ', 'sˠuulʲ', 'validate']))
        self.assertEqual(words[735], MainDataset.Word._make([
            'gle', 'iris1253', 'allein::ADV', 'i d\'aonar', 'ɪd̪ˠiːn̪ˠəɾˠ', 'ɪdˠiinˠəɾˠ', 'validate']))
