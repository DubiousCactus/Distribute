'''
This class holds the strategy parameters, parsed from the config
'''


class Strategy:

    def __init__(self, config, strat=None):
        if not strat:
            choice = config['strategy']
        else:
            choice = strat
        self.description = config['strategies'][choice]['desc']
        self.coding = config['strategies'][choice]['coding']
        self.replicas = config['strategies'][choice]['replicas']
        self.losses = config['strategies'][choice]['coding']

