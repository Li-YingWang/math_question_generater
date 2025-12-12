from core.base_plugin import BasePlugin
from core.utils import format_latex, NumberGenerator
from fractions import Fraction

class SubstractionPlugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "減法(國中)"

    def generate(self, count):
        number_format = getattr(self, "number_format", "integer")
        amplitude = getattr(self, "amplitude", 100)
        num_gen = NumberGenerator(
            number_format=number_format,
            amplitude=amplitude,
            decimal_places=2,
            allow_negative=True,
            fraction_simplify=True
        )

        returns = []
        for _ in range(count):
            a, a_text = num_gen.generate()
            b, b_text = num_gen.generate()
            while a > b > 0:
                a, a_text = num_gen.generate()
                b, b_text = num_gen.generate()

            a_text = f"({a_text})" if a < 0 else a_text
            b_text = f"({b_text})" if b < 0 else b_text

            question = a_text + "-" + b_text
            if number_format == "decimal":
                answer = f"{round(a - b, 2):.2f}"
            elif number_format == "fraction":
                ans = Fraction(a - b)
                if ans.denominator == 1:
                    answer = f"{ans.numerator}"
                elif ans.numerator < 0:
                    answer = f"-\\frac{{{abs(ans.numerator)}}}{{{ans.denominator}}}"
                else:
                    answer = f"\\frac{{{ans.numerator}}}{{{ans.denominator}}}"
            else:
                answer = str(a - b)
            returns.append((format_latex(question), format_latex(answer)))
        return returns

def get_plugin():
    return SubstractionPlugin()