from collections import OrderedDict
from pprint import pprint


class Weigher:
    def __init__(self, strategies):
        self.strategies = strategies

    def get_weighed(self) -> []:
        """ Gets distinct tickers from each of the strategies
            then gets their rebalancedWeight or 0
            and divides that by the strategy count

            Returns: dict of assets with strategy and combined_weight values, eg
            'ADA': {'BLX': 0.0539, 'CAR': 0.0, 'ECA': 0.0, 'combined_weight': 0.017},
            'ALGO': {'BLX': 0.0078, 'CAR': 0.03, 'ECA': 0.0, 'combined_weight': 0.013},

         """

        assets = {}
        strategy_names = []

        for strategy in self.strategies:
            # fill the assets with asset tickers and their weights
            strategy_name = strategy["ticker"]
            strategy_names.append(strategy_name)
            strategy_assets = strategy["values"]

            for asset in strategy_assets:
                # some strategies have invalid values
                if "assetTicker" not in asset:
                    continue

                weight = asset["rebalancedWeight"]
                asset_ticker = asset["assetTicker"]

                if asset_ticker in assets:
                    assets[asset_ticker][strategy_name] = weight
                else:
                    assets[asset_ticker] = {strategy_name: weight}

        for asset in assets.values():
            # calculate the average weight
            for strategy_name in strategy_names:
                if strategy_name not in asset:
                    asset[strategy_name] = 0.0
            asset["combined_weight"] = sum(asset.values()) / len(self.strategies)

        sorted_assets = sorted(assets.items(), key=lambda it: it[1]["combined_weight"], reverse=True)
        return OrderedDict(sorted_assets)
