from fractions import Fraction
from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin

class DivisionPlugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "除法(國中)"

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
            while (b == 0) or ((a > 0) and (b > 0)):
                a, a_text = num_gen.generate()
                b, b_text = num_gen.generate()

            str_a = f"({a_text})" if a < 0 else a_text
            str_b = f"({b_text})" if b < 0 else b_text

            question = str_a + " \\div " + str_b
            if number_format == "decimal":
                ans_num = round(a * 100)
                ans_den = round(b * 100)
                frac = Fraction(ans_num, ans_den)
            else:
                frac = Fraction(a, b)
            if frac.denominator == 1:
                answer = f"{frac.numerator}"
            elif frac.numerator < 0:
                answer = f"-\\frac{{{abs(frac.numerator)}}}{{{frac.denominator}}}"
            else:
                answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return DivisionPlugin()