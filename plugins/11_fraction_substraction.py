from fractions import Fraction
from plugins.general import generate_nums, format_latex
from core.base_plugin import BasePlugin

class FractionSubstractionPlugin(BasePlugin):
    def __init__(self, amplitude=100):
        self.amplitude = amplitude

    def get_name(self):
        return "分數減法(國中)"

    def generate(self, count):
        returns = []
        for _ in range(count):
            a, b, c, d = generate_nums(4, self.amplitude)
            while (b == 0) or (d == 0) or (((a * b) >= 0) and ((c * d) >= 0)) or (Fraction(a, b).denominator == 1) or (Fraction(c, d).denominator == 1):
                a, b, c, d = generate_nums(4, self.amplitude)

            frac_a = Fraction(a, b)
            frac_b = Fraction(c, d)

            if frac_a.numerator < 0:
                str_a = f"(-\\frac{{{abs(frac_a.numerator)}}}{{{frac_a.denominator}}})"
            else:
                str_a = f"\\frac{{{frac_a.numerator}}}{{{frac_a.denominator}}}"
            if frac_b.numerator < 0:
                str_b = f"(-\\frac{{{abs(frac_b.numerator)}}}{{{frac_b.denominator}}})"
            else:
                str_b = f"\\frac{{{frac_b.numerator}}}{{{frac_b.denominator}}}"

            question = f"{str_a}-{str_b}"

            frac_answer = frac_a - frac_b

            if frac_answer.denominator == 1:
                answer_str = f"{frac_answer.numerator}"
            elif frac_answer.numerator < 0:
                answer_str = f"(-\\frac{{{abs(frac_answer.numerator)}}}{{{frac_answer.denominator}}})"
            else:
                answer_str = f"\\frac{{{frac_answer.numerator}}}{{{frac_answer.denominator}}}"
            returns.append((format_latex(question), format_latex(answer_str)))
        return returns

def get_plugin():
    return FractionSubstractionPlugin()