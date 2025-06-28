'''Parsing for ingredients'''

from dataclasses import dataclass
from fractions import Fraction

@dataclass
class IngredientLineItem:
    quantity: float
    unit: str
    name: str

class IngredientList:
    def __init__(self, lst: str):
        self.lst = lst
        self.parsed: list[IngredientLineItem] = self.parse()

    def parse_quantity(self, tokens: list[str]) -> tuple[float, list[str]]:
        """
        Parses quantity from the beginning of the token list.
        Handles integers, simple fractions, and mixed fractions.
        Returns a float quantity and the remaining tokens.
        """
        if len(tokens) >= 2 and '/' in tokens[1]:
            # Possibly a mixed fraction
            try:
                whole = int(tokens[0])
                frac = Fraction(tokens[1])
                quantity = float(whole + frac)
                return quantity, tokens[2:]
            except (ValueError, ZeroDivisionError):
                pass  # Fall through

        try:
            # Try parsing just the first token
            quantity = float(Fraction(tokens[0]))
            return quantity, tokens[1:]
        except (ValueError, ZeroDivisionError):
            raise ValueError(f"Invalid quantity format: {' '.join(tokens[:2])}")

    def parse(self):
        lines = self.lst.strip().split('\n')
        master = []
        for line in lines:
            tokens = line.strip().split()
            if not tokens:
                continue

            quantity, rest = self.parse_quantity(tokens)
            assert len(rest) >= 2, f"Malformed line after quantity: '{line}'"
            unit = rest[0]
            name = ' '.join(rest[1:])
            master.append(IngredientLineItem(quantity, unit, name))
        return master

    def __str__(self):
        return '\n'.join(f"{item.quantity} {item.unit} {item.name}" for item in self.parsed)
