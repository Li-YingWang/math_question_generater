import random
from fractions import Fraction

def generate_nums(num_count: int, amplitude=100) -> list:
    return [random.randint(-amplitude, amplitude) for _ in range(num_count)]

def format_latex(expr):
    return f"${expr}$"

class NumberGenerator:
    def __init__(
        self,
        number_format="integer",     # integer | fraction | decimal
        amplitude=100,
        decimal_places=2,
        fraction_simplify=True,
        allow_negative=True,
        allow_zero=True
    ):
        self.number_format = number_format
        self.amplitude = amplitude
        self.decimal_places = decimal_places
        self.fraction_simplify = fraction_simplify
        self.allow_negative = allow_negative
        self.allow_zero = allow_zero

    def rand_int(self):
        a, b = -self.amplitude, self.amplitude
        n = random.randint(a, b)
        if not self.allow_negative:
            n = abs(n)
        return n, str(n)

    def rand_decimal(self):
        a, b = -self.amplitude, self.amplitude
        raw = random.uniform(a, b)
        if not self.allow_negative:
            raw = abs(raw)

        value = round(raw, self.decimal_places)
        text = f"{value:.{self.decimal_places}f}"
        return value, text

    def rand_fraction(self):
        a, b = -self.amplitude, self.amplitude
        numerator = random.randint(a, b)
        denominator = random.randint(a, b)

        # 避免除以 0
        while denominator == 0:
            denominator = random.randint(a, b)

        if not self.allow_negative:
            numerator = abs(numerator)
            denominator = abs(denominator)

        frac = Fraction(numerator, denominator)

        if frac.denominator == 1:
            return frac.numerator, str(frac.numerator)
        elif frac < 0:
            text = f"-\\frac{{{abs(frac.numerator)}}}{{{abs(frac.denominator)}}}"
        else:
            text = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"

        return frac, text

    def generate(self):
        if self.number_format == "integer":
            return self.rand_int()
        elif self.number_format == "decimal":
            return self.rand_decimal()
        elif self.number_format == "fraction":
            return self.rand_fraction()
        else:
            raise ValueError(f"Unknown number_format: {self.number_format}")
