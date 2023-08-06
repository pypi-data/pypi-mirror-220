class Profile:
    def __init__(self):
        self.holding = {}
        self.balance = 0
        self.cash = 0

    def update(self, symbol: str, quantity: int, price: float):
        if symbol in self.holding:
            self.holding[symbol] += quantity
        else:
            self.holding[symbol] = quantity
        self.cash -= (quantity * price)