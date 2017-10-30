from unittest import TestCase

from classifier import evalute_https_score, evalute_performance_score, evalute_trust_score

class TestClassifier(TestCase):
    def test_evalute_https_score(self):
        self.assertEqual(True, True)

    def test_wrong_https_file(self):
        """questo test deve fallire se il file non esiste"""
        map_file_name = 'data.txt'
        self.assertFalse(evalute_https_score(map_file_name))

    def test_invalid_https_file(self):
        """questo test deve fallire se sbaglio il nome del file
        che deve essere pshtt.csv"""
        map_file_name = 'data.csv'
        self.assertFalse(evalute_https_score(map_file_name))


    def test_wrong_pageload_file(self):
        """questo test deve fallire se il file non esiste"""
        map_file_name = 'data.txt'
        self.assertFalse(evalute_performance_score(map_file_name))

    def test_invalid_pageload_file(self):
        """questo test deve fallire se sbaglio il nome del file
        che deve essere pageload.csv"""
        map_file_name = 'data.csv'
        self.assertFalse(evalute_performance_score(map_file_name))

    def test_wrong_trust_file(self):
        """questo test deve fallire se il file non esiste"""
        map_file_name = 'data.txt'
        self.assertFalse(evalute_trust_score(map_file_name))

    def test_invalid_trust_file(self):
        """questo test deve fallire se sbaglio il nome del file
        che deve essere trust.csv"""
        map_file_name = 'data.csv'
        self.assertFalse(evalute_trust_score(map_file_name))
