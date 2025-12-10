from fractions import Fraction
from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin

class Equation4Plugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "一元一次方程式(ax+b=cx+d)"

    def generate(self, count):
        number_format = getattr(self, "number_format", "integer")
        amplitude = getattr(self, "amplitude", 100)
        returns = []
        for _ in range(count):
            num_gen = NumberGenerator(
                number_format=number_format,
                amplitude=amplitude,
                decimal_places=2,
                allow_negative=True,
                fraction_simplify=True
            )
            a, a_text = num_gen.generate()
            b, b_text = num_gen.generate()
            c, c_text = num_gen.generate()
            d, d_text = num_gen.generate()
            while (0 in [a, b, c, d]) or (a == c) or (b == d):
                a, a_text = num_gen.generate()
                b, b_text = num_gen.generate()
                c, c_text = num_gen.generate()
                d, d_text = num_gen.generate()

            x1 = "x" if a == 1 else "-x" if a == -1 else f"{a_text}x"
            b1 = f"+{b_text}" if b > 0 else b_text
            x2 = "x" if c == 1 else "-x" if c == -1 else f"{c_text}x"
            d1 = f"+{d_text}" if d > 0 else d_text

            question = f"{x1}{b1}={x2}{d1}"
            answer = f"{(d - b) // (a - c)}" if (d - b) % (a - c) == 0 else None
            if answer is None:
                frac = Fraction(d - b, a - c)
                answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return Equation4Plugin()