from fractions import Fraction
from plugins.general import generate_nums, format_latex
from core.base_plugin import BasePlugin

class Equation4Plugin(BasePlugin):
    def __init__(self, amplitude=100):
        self.amplitude = amplitude

    def get_name(self):
        return "一元一次方程式(ax+b=cx+d)"

    def generate(self, count):
        returns = []
        for _ in range(count):
            a, b, c, d = generate_nums(4, self.amplitude)
            while (0 in [a, b, c, d]) or (a == c) or (b == d):
                a, b, c, d = generate_nums(4, self.amplitude)

            x1 = "x" if a == 1 else "-x" if a == -1 else f"{a}x"
            b1 = f"+{b}" if b > 0 else str(b)
            x2 = "x" if c == 1 else "-x" if c == -1 else f"{c}x"
            d1 = f"+{d}" if d > 0 else str(d)

            question = f"{x1}{b1}={x2}{d1}"
            answer = f"{(d - b) // (a - c)}" if (d - b) % (a - c) == 0 else None
            if answer is None:
                frac = Fraction(d - b, a - c)
                answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return Equation4Plugin()