class Publisher:
    def __init__(self):
        self._observers = set()

    def notify(self):
        for observer in self._observers:
            observer.changed(self)

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)