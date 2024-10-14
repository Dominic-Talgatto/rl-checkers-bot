class Move:
    def __init__(self, initial, final) -> None:
        self.initial = initial     #Squares
        self.final = final

    def __eq__(self, other) -> bool:
        return self.initial == other.initial and self.final == other.final