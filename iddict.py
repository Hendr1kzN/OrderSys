class IDDict(dict):
    def __init__(self):
        super().__init__()
        self.counter = 0
    
    def set(self, value) -> int:
        self.counter += 1
        super().__setitem__(self.counter, value)
        return self.counter