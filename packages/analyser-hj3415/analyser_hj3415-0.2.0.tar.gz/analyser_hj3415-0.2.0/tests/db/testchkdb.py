import unittest
from src.analyser_hj3415.db import chk_db
from src.analyser_hj3415.db import mongo

addr = "mongodb://192.168.0.173:27017"
client = mongo.connect_mongo(addr)


class ChkDBTest(unittest.TestCase):
    def test_chk_integrity_cxxx(self):
        print(chk_db.chk_integrity_corps(client, '005930'))

    def test_chk_integrity_cxxx_all(self):
        print(chk_db.chk_integrity_corps(client, 'all'))