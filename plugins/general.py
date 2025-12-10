import random

def generate_nums(num_count: int, amplitude=100) -> list:
    return [random.randint(-amplitude, amplitude) for _ in range(num_count)]

def format_latex(expr):
    return f"${expr}$"
