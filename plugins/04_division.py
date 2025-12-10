from fractions import Fraction
from plugins.general import generate_nums, format_latex
from core.base_plugin import BasePlugin

class DivisionPlugin(BasePlugin):
    def __init__(self, amplitude=100):
        self.amplitude = amplitude

    def get_name(self):
        return "整數除法(國中)"

    def generate(self, count):
        returns = []
        for _ in range(count):
            a, b = generate_nums(2, self.amplitude)
            while (b == 0) or ((a > 0) and (b > 0)):
                a, b = generate_nums(2, self.amplitude)

            str_a = f"({a})" if a < 0 else str(a)
            str_b = f"({b})" if b < 0 else str(b)

            question = str_a + " \\div " + str_b
            if a % b == 0:
                answer = str(a // b)
            else:
                frac = Fraction(a, b)
                answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return DivisionPlugin()