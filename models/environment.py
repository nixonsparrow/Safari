class Plant:
    def __init__(self, eatable=False, obstacle=False):
        self.eatable = eatable
        self.obstacle = obstacle
        self.symbol = 'T' if obstacle else '.'
        self.kingdom = 'plant'
