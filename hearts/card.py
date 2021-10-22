class Card:
    def __init__(self, face: 'FACE', suit: 'SUIT') -> None:
        self.face = face
        self.suit = suit

    def __str__(self) -> str:
        return f'{self.suit.value}{self.face.value}'

    def __repr__(self):
        return self.__str__()

    def __key(self):
        return self.face, self.suit

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        if isinstance(other, Card):
            return self.__key() == other.__key()
        return NotImplemented

