import random
from fractions import Fraction

class QuestionGenerator:
    def __init__(self):
        pass

    def generate_nums(self, num_count: int, amplitude=100) -> list:
        return [random.randint(-amplitude, amplitude) for _ in range(num_count)]

    def format_latex(self, expr):
        return f"${expr}$"

    def generate_addition(self, amplitude=100):
        a, b = self.generate_nums(2, amplitude)
        while (a > 0) and (b > 0):
            a, b = self.generate_nums(2, amplitude)

        str_a = f"({a})" if a < 0 else str(a)
        str_b = f"({b})" if b < 0 else str(b)

        question = str_a + "+" + str_b
        answer = str(eval(question))
        return self.format_latex(question), self.format_latex(answer)

    def generate_substraction(self, amplitude=100):
        a, b = self.generate_nums(2, amplitude)
        while a > b > 0:
            a, b = self.generate_nums(2, amplitude)

        str_a = f"({a})" if a < 0 else str(a)
        str_b = f"({b})" if b < 0 else str(b)

        question = str_a + "-" + str_b
        answer = str(eval(question))
        return self.format_latex(question), self.format_latex(answer)

    def generate_multiplication(self, amplitude=100):
        a, b = self.generate_nums(2, amplitude)
        while (a >= 0) and (b >= 0):
            a, b = self.generate_nums(2, amplitude)

        str_a = f"({a})" if a < 0 else str(a)
        str_b = f"({b})" if b < 0 else str(b)

        question = str_a + " \\times " + str_b
        answer = str(a * b)
        return self.format_latex(question), self.format_latex(answer)

    def generate_division(self, amplitude=100):
        a, b = self.generate_nums(2, amplitude)
        while (b == 0) or ((a > 0) and (b > 0)):
            a, b = self.generate_nums(2, amplitude)

        str_a = f"({a})" if a < 0 else str(a)
        str_b = f"({b})" if b < 0 else str(b)

        question = str_a + " \\div " + str_b
        if a % b == 0:
            answer = str(a // b)
        else:
            frac = Fraction(a, b)
            answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
        return self.format_latex(question), self.format_latex(answer)

    def generate_linear_equation_1(self, amplitude=100):
        a, b = self.generate_nums(2, amplitude)
        while a == 0:
            a, b = self.generate_nums(2, amplitude)

        question = f"x+{a}={b}" if a > 0 else f"x{a}={b}"
        answer = f"{b - a}"
        return self.format_latex(question), self.format_latex(answer)
    
    def generate_linear_equation_2(self, amplitude=100):
        a, b = self.generate_nums(2, amplitude)
        while (a in [0, 1]) or (b == 0):
            a, b = self.generate_nums(2, amplitude)
        
        question = f"{a}x={b}"
        answer = f"{b // a}" if b % a == 0 else None
        if answer is None:
            frac = Fraction(b, a)
            answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
        return self.format_latex(question), self.format_latex(answer)

    def generate_linear_equation_3(self, amplitude=100):
        a, b, c = self.generate_nums(3, amplitude=amplitude)
        while (a in [0, 1]) or (b == 0):
            a, b, c = self.generate_nums(3, amplitude)

        question = f"{a}x+{b}={c}" if b > 0 else f"{a}x{b}={c}"
        answer = f"{(c - b) // a}" if (c - b) % a == 0 else None
        if answer is None:
            frac = Fraction(c - b, a)
            answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
        return self.format_latex(question), self.format_latex(answer)

    def generate_linear_equation_4(self, amplitude=100):
        a, b, c, d = self.generate_nums(4, amplitude)
        while (0 in [a, b, c, d]) or (a == c) or (b == d):
            a, b, c, d = self.generate_nums(4, amplitude)

        x1 = "x" if a == 1 else "-x" if a == -1 else f"{a}x"
        b1 = f"+{b}" if b > 0 else str(b)
        x2 = "x" if c == 1 else "-x" if c == -1 else f"{c}x"
        d1 = f"+{d}" if d > 0 else str(d)

        question = f"{x1}{b1}={x2}{d1}"
        answer = f"{(d - b) // (a - c)}" if (d - b) % (a - c) == 0 else None
        if answer is None:
            frac = Fraction(d - b, a - c)
            answer = f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
        return self.format_latex(question), self.format_latex(answer)
