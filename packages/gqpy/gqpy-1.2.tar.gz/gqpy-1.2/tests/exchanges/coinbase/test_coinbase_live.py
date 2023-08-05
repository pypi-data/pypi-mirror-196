# Importing external libraries
import sys
import unittest

# Importing libraries we want to test
sys.path.append('../../../')
import libs.python.src.gqpy.gqpy as gq

class TestCoinbaseLive(unittest.TestCase):

    def setUp(self):
        
        self.gq = gq.GoQuant()
        self.exchange = 'coinbase'

    def test_ticker(self):

        symbol_pair = 'BTC-USD'

        res = self.gq.live.ticker(self.exchange, symbol_pair, False, 5)

        # Ensuring the correct type was returned
        self.assertEqual(list, type(res))
        self.assertTrue(len(res) > 0)

        # Ensuring the correct format was returned
        dp = res[-1]
        self.assertEqual(dict, type(dp))
        self.assertEqual(dp['assetClass'], 'spot')
        self.assertEqual(dp['channel'], 'coinbase.spot.ticker.BTC-USD')

    def test_book(self):

        symbol_pair = 'BTC-USD'

        res = self.gq.live.book(self.exchange, symbol_pair, False, 5)
        
        self.assertEqual(list, type(res))
        self.assertTrue(len(res) > 0)

        dp = res[-1]
        self.assertEqual(dict, type(dp))
        self.assertEqual(dp['assetClass'], 'spot')
        self.assertEqual(dp['channel'], 'coinbase.spot.book.BTC-USD')

    def test_trade(self):

        symbol_pair = 'BTC-USD'

        res = self.gq.live.trade(self.exchange, symbol_pair, False, 5)
        self.assertEqual(list, type(res))

        self.assertEqual(list, type(res))
        self.assertTrue(len(res) > 0)

        dp = res[-1]
        self.assertEqual(dict, type(dp))
        self.assertEqual(dp['assetClass'], 'spot')
        self.assertEqual(dp['channel'], 'coinbase.spot.trade.BTC-USD')

if __name__ == "__main__":
    unittest.main()