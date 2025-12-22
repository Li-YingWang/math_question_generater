from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin
from fractions import Fraction

class CrossMultiplyQuadA1Plugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "解一元二次方程式"

    def generate(self, count):
        number_format = getattr(self, "number_format", "integer")
        amplitude = getattr(self, "amplitude", 10)

        num_gen = NumberGenerator(
            number_format=number_format,
            amplitude=amplitude,
            decimal_places=2,
            allow_negative=True,
            fraction_simplify=True,
        )

        results = []
        for _ in range(count):
            # 產生 3 個整數
            a, a_text = num_gen.generate()
            b, b_text = num_gen.generate()
            c, c_text = num_gen.generate()

            while 0 in [a, b, c]:
                a, a_text = num_gen.generate()
                b, b_text = num_gen.generate()
                c, c_text = num_gen.generate()

            # 化簡 a, b, c 的最大公因數
            from math import gcd
            if number_format == "integer":
                gcd_abc = gcd(abs(a), abs(b), abs(c))
                if gcd_abc > 1:
                    a //= gcd_abc
                    b //= gcd_abc
                    c //= gcd_abc

            # 組出題目字串，處理正負號顯示
            a_part = f"x^2" if a == 1 else f"-x^2" if a == -1 else f"{a}x^2"
            b_part = f"+x" if b == 1 else f"-x" if b == -1 else f"+{b}x" if b > 0 else "" if b == 0 else f"{b}x"
            c_part = f"+{c}" if c > 0 else str(c)

            question = f"{a_part}{b_part}{c_part}=0"
            
            # 
            if number_format == "fraction":
                from math import lcm
                lcm_denominator = lcm(abs(a.denominator), abs(b.denominator), abs(c.denominator))
                a *= lcm_denominator
                b *= lcm_denominator
                c *= lcm_denominator
                a = a.numerator
                b = b.numerator
                c = c.numerator
            elif number_format == "decimal":
                a = int(round(a * 100))
                b = int(round(b * 100))
                c = int(round(c * 100))

            # 組答案 x= (-b±√(b²-4ac))/(2a)
            discriminant = b**2 - 4 * a * c

            if discriminant < 0:
                answer = "無實數解"
            else:
                from math import isqrt
                print(format(a), format(b), format(c), format(discriminant))
                sqrt_discriminant = isqrt(discriminant)
                if sqrt_discriminant * sqrt_discriminant == discriminant:
                    root1_numerator = -b + sqrt_discriminant
                    root2_numerator = -b - sqrt_discriminant
                    denominator = 2 * a

                    def format_root(numerator, denominator):
                        frac = Fraction(numerator, denominator)
                        if frac.denominator == 1:
                            return str(frac.numerator)
                        elif frac.numerator < 0:
                            return f"-\\frac{{{abs(frac.numerator)}}}{{{frac.denominator}}}"
                        else:
                            return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"

                    root1 = format_root(root1_numerator, denominator)
                    root2 = format_root(root2_numerator, denominator)

                    if root1 == root2:
                        answer = root1
                    else:
                        answer = f"{root1}, {root2}"
                else:
                    answer = f"\\frac{{{-b} \\pm \\sqrt{{{discriminant}}}}}{{{2*a}}}"

            results.append((format_latex(question), format_latex(answer) if answer != "無實數解" else answer))

        return results


def get_plugin():
    return CrossMultiplyQuadA1Plugin()
