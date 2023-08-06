from collections import Counter

from colorama import Fore, Style

from src.analysis.config import ColorConfig


class CodeSmell:
    def __init__(self,
                 code_smell_id,
                 code_smell_title,
                 file_path=None,
                 line=None,
                 col_offset=None,
                 smell_type=None,
                 description=None,
                 pipeline_stage=None,
                 effect=None,
                 source_code=None,
                 source_astroid_node=None):
        self.code_smell_id = code_smell_id
        self.code_smell_title = code_smell_title
        self.file_path = file_path
        self.line = line
        self.col_offset = col_offset
        self.smell_type = smell_type
        self.description = description
        self.pipeline_stage = pipeline_stage
        self.effect = effect
        self.source_code = source_code
        self.source_astroid_node = source_astroid_node

    def __repr__(self):
        code_snippet = self.source_code[:60] + '...' if len(self.source_code) > 60 else self.source_code
        enable_color = ColorConfig.get_instance().enable_color
        if enable_color:
            return (
                f"{Fore.GREEN}{self.file_path}:{self.line}:{self.col_offset}: "
                f"{Fore.YELLOW}[{self.code_smell_id}] {self.code_smell_title} "
                f"{Fore.CYAN}[Stage: {self.pipeline_stage}, Effect: {self.effect}, Type: {self.smell_type}] "
                f"Code: {code_snippet}{Style.RESET_ALL}"
            )
        else:
            return (
                f"{self.file_path}:{self.line}:{self.col_offset}: "
                f"[{self.code_smell_id}] {self.code_smell_title} "
                f"[Stage: {self.pipeline_stage}, Effect: {self.effect}, Type: {self.smell_type}] "
                f"Code: {code_snippet}"
            )


class Result:
    """
    Representing the analysis result of a python file.
    """

    code_smells = []

    @staticmethod
    def add(code_smell: CodeSmell) -> None:
        Result.code_smells.append(code_smell)

    @staticmethod
    def calc_n_files_had_code_smell() -> int:
        if Result.code_smells:
            return len(set(obj.file_path for obj in Result.code_smells))

        return 0

    @staticmethod
    def print_n_unique_code_smell_occurrence():
        if Result.code_smells:
            print(dict(Counter(obj.code_smell_id for obj in Result.code_smells)))
        else:
            print({})

    @staticmethod
    def print_code_smells():
        if not Result.code_smells:
            return

        for code_smell in Result.code_smells:
            print(code_smell)

    @staticmethod
    def print_project_stats(file_count, file_syntax_error_count):
        n_total = len(Result.code_smells)
        n_csa = len([smell for smell in Result.code_smells if 'CSA' in smell.code_smell_id])
        n_cs = n_total - n_csa

        print("# .py files in project:", file_count)
        print("# .py files detected code smells:", Result.calc_n_files_had_code_smell())
        print("# .py files could not be parsed/syntax error:", file_syntax_error_count)
        print("# code smells:", n_cs)
        print("# code smells advice:", n_csa)
        print("# total smells:", n_total)

    @staticmethod
    def print_code_smell_stats():
        Result.print_n_unique_code_smell_occurrence()
