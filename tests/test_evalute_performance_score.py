from unittest import TestCase
from score import evalute_performance_score


class TestEvalute_performance_score(TestCase):
    def test__load_csv_wrong(self):
        """deve fallire se il file csv non esiste"""
        map_file_name = 'csv/wrong.csv'
        evalute_performance_score(map_file_name)
        self.fail()

    #def test_evalute_performance_score(self):
    #    self.fail()
