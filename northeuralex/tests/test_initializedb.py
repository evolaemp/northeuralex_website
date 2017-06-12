import os.path
import unittest

from northeuralex.scripts.initializedb import LangDataset, MainDataset



FIXTURES_DIR = 'northeuralex/tests/fixtures'



class LangDatasetTestCase(unittest.TestCase):

    def setUp(self):
        self.dataset = LangDataset(os.path.join(FIXTURES_DIR, 'lang_data.tsv'))

    def test_gen_langs(self):
        langs = []
        for lang in self.dataset.gen_langs():
            self.assertTrue(type(lang) is LangDataset.Language)
            langs.append(lang)

        self.assertEqual(len(langs), 509)

        self.assertEqual(langs[0], LangDataset.Language._make([
            'aaa', 'ghot1243', '7.11551', '5.95663', 'Ghotuo']))
        self.assertEqual(langs[7], LangDataset.Language._make([
            'aah', 'abua1245', '', '', 'Abu\' Arapesh']))
        self.assertEqual(langs[-1], LangDataset.Language._make([
            'azz', 'high1278', '20.1554', '-97.5556', 'Highland Puebla Nahuatl']))



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
