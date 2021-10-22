class Card:
    def __init__(self, face: 'FACE', suit: 'SUIT') -> None:
        self.face = face
        self.suit = suit

    def __str__(self) -> str:
        return f'{self.suit.value[0]}{self.face.value}'

    def __repr__(self):
        return self.__str__()
