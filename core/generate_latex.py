class LatexBuilder:

    def __init__(self, template_path: str, output_path: str, max_questions_per_page: int = 20):
        self.template_path = template_path
        self.output_path = output_path
        self.max_questions_per_page = max_questions_per_page  # 每頁顯示的題目數量
        with open(self.template_path, "r", encoding="utf-8") as f:
            self.template = f.read()

    def build_latex_content(self, pages_data: list[list[tuple[str, str]]]) -> str:
        problems_section = ""
        all_answers = []

        problems_section += "\\begin{problems}[label=(\\arabic*)]\n"
        for page_index, qa_pairs in enumerate(pages_data):
            for q, a in qa_pairs:
                problems_section += f"  \\item {q}\n"
                all_answers.append(a)
            problems_section += "\\clearpage\n\\newpage\n"
        problems_section += "\\end{problems}\n\n"

        answers_section = "\\begin{enumerate}[itemsep=1em, leftmargin=*, label=(\\arabic*)]\n"
        for i in range(0, len(all_answers), 5):
            item_num = i + 1
            line = " \\quad ".join(all_answers[i:i+5])
            answers_section += (
                f"  \\setcounter{{enumi}}{{{item_num - 1}}}\n"
                f"  \\item {line}\n"
            )
        answers_section += "\\end{enumerate}\n"

        final_tex = self.template.replace("% QUESTIONS_HERE", problems_section).replace("% ANSWERS_HERE", answers_section)
        
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(final_tex)
        
        return self.output_path
