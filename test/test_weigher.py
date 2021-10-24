import json
from pprint import pprint

from weigher import Weigher


def test_get_weighed():
    # weighter gets distinct tickers from each of the strategies
    # then gets their rebalancedWeight or 0
    # and divides those by the strategy count
    top_three_file = open("top-three.json")
    top_three = json.load(top_three_file)

    weigher = Weigher(top_three)
    weighed = weigher.get_weighed()

    # for btc, the weights from 3 strategies are
    # "rebalancedWeight": 0.3,
    # "rebalancedWeight": 0.1,
    # "rebalancedWeight": 0.4,
    # combined should be (0.3+0.1+0.4) / 3 = 0.266667

    assert (weighed["BTC"]["combined_weight"] == 0.26666666666666666)


def test_ten_strategies():
    file = open("top-ten.json")
    json_strategies = json.load(file)

    weigher = Weigher(json_strategies)
    weighed = weigher.get_weighed()
    pprint(weighed)
