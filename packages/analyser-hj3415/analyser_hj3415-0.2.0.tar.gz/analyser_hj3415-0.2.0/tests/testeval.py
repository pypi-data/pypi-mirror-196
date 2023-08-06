import random
import unittest
import pprint
from src.analyser_hj3415 import eval
from src.analyser_hj3415.db import mongo


addr = "mongodb://192.168.0.173:27017"
client = mongo.connect_mongo(addr)
all_codes = mongo.Corps.get_all_codes(client)


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.test_code = '005930'

    def tearDown(self):
        """테스트 종료 후 파일 삭제 """
        pass

    def test_red(self):
        # 특정 한 종목
        print(self.test_code, '/', mongo.Corps.get_name(client, self.test_code))
        pprint.pprint(eval.red(client, self.test_code))

    def test_red_all(self):
        # 디비 안 전체 종목
        print(f'Totol {len(all_codes)} items')
        for i, code in enumerate(all_codes):
            print(i, '/', code, '/', mongo.Corps.get_name(client, code))
            print(eval.red(client, code))

    def test_blue(self):
        # 특정 한 종목
        print(self.test_code, '/', mongo.Corps.get_name(client, self.test_code))
        pprint.pprint(eval.blue(client, self.test_code))

    def test_blue_all(self):
        # 디비 안 전체 종목
        print(f'Totol {len(all_codes)} items')
        for i, code in enumerate(all_codes):
            print(i, '/', code, '/', mongo.Corps.get_name(client, code))
            print(eval.blue(client, code))

    def test_mil(self):
        # 특정 한 종목
        print(self.test_code, '/', mongo.Corps.get_name(client, self.test_code))
        pprint.pprint(eval.mil(client, self.test_code))

    def test_mil_all(self):
        # 디비 안 전체 종목
        print(f'Totol {len(all_codes)} items')
        for i, code in enumerate(all_codes):
            print(i, '/', code, '/', mongo.Corps.get_name(client, code))
            print(eval.mil(client, code))






"""
    def test_one(self):
        # 한 종목 전부다
        print('/'.join([str(1), self.code]))
        print(red(self.client, self.code))

        pp = pprint.PrettyPrinter(width=200)
        pp.pprint(mil(self.client, self.code))
        pp.pprint(blue(self.client, self.code))
        pprint.pprint(growth(self.client, self.code), width=150)


    def test_growth(self):
        # 특정 한 종목
        pprint.pprint(growth(self.client, self.code), width=150)

        # 디비 안 전체 종목
        for i, code in enumerate(self.codes[:]):
            print('/'.join([str(i), str(code)]))
            pprint.pprint(growth(self.client, code), width=150)
"""

class GetDFTest(unittest.TestCase):
    def test_make_df_part(self):
        codes = ['025320', '000040', '060280', '003240']
        from multiprocessing import Queue
        q = Queue()
        _make_df_part(dbpath.load(), codes, q)

    def test_get_df(self):
        print(make_today_eval_df(db_addr=dbpath.load()))


class SpacTest(unittest.TestCase):
    def setUp(self):
        self.client = mongo2.connect_mongo(dbpath.load())

    def test_valid_spac(self):
        for code, name, price in yield_valid_spac(self.client):
            print(code, name, price)
