from abc import abstractmethod, ABC

class ObjectGame(ABC):
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass