from core.utils import format_latex, NumberGenerator
from core.base_plugin import BasePlugin

class CrossMultiplyQuadA1Plugin(BasePlugin):
    def __init__(self):
        pass

    def get_name(self):
        return "十字交乘法因式分解（二次項係數為 1）"

    def generate(self, count):
        # 此題型專注於整數因式分解，若 UI 選擇非整數格式則退回到整數模式
        number_format = getattr(self, "number_format", "integer")
        if number_format != "integer":
            number_format = "integer"

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
            # 產生兩個整數作為因數 m, n，使得多項式為 x^2 + (m+n)x + m*n
            m, m_text = num_gen.generate()
            n, n_text = num_gen.generate()

            # 避免過於簡單或重複的題目（例如 m 或 n 為 0 可接受，但可選擇避免）
            # 若需要，可以加入更多限制；目前允許任何整數
            while 0 in [m, n]:
                m, m_text = num_gen.generate()
                n, n_text = num_gen.generate()

            b = m + n
            c = m * n

            # 組出題目字串，處理正負號顯示
            b_part = f"+{b}x" if b > 0 else f"{str(b)}x" if b < 0 else ""
            c_part = f"+{c}" if c > 0 else str(c) if c < 0 else ""

            # 特殊情況：若 b == 0 或 c == 0，確保形式正確（例如 x^2+0x+3 -> x^2+3）
            question = f"x^2{b_part}{c_part}"

            # 組答案 (x + m)(x + n)
            def factor_term(v):
                if v > 0:
                    return f"(x+{v})"
                elif v < 0:
                    return f"(x{v})"  # v already includes the minus sign
                else:
                    return "x"

            term_m = factor_term(m)
            term_n = factor_term(n)

            answer = f"{term_m}{term_n}"

            results.append((format_latex(question), format_latex(answer)))

        return results


def get_plugin():
    return CrossMultiplyQuadA1Plugin()
