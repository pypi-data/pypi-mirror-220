import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class UnnecessaryIteration(BaseChecker):
    """
    This class verifies the presence of "pandas" and "tensorflow" import statements, tracks the occurrence of
    for-loop and while-loop constructs, and applies a depth-first search within these loop statements to identify
    instances of "pandas" or "tensorflow" as inferred strings.
    """

    ID = "CSA1"
    TITLE = "Avoid unnecessary iterations. Use vectorized solutions instead of loops."
    DESCRIPTION = """
    Context:
    Loops are typically time-consuming and verbose, while
    developers can usually use some vectorized solutions to replace the
    loops.

    Problem:
    As stated in the Pandas documentation: “Iterating
    through pandas objects is generally slow. In many cases, iterating
    manually over the rows is not needed and can be avoided”. It
    is also stated that the slicing operation with loops in TensorFlow is
    slow, and there is a substitute for better performance.

    Solution:
    Machine learning applications are typically data-intensive,
    requiring operations on data sets rather than an individual
    value. Therefore, it is better to adopt a vectorized solution
    instead of iterating over data. In this way, the program runs faster
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.has_import: bool = False
        self.code_smell_found: bool = False

    def visit_import(self, node: astroid.Import) -> None:
        if self.code_smell_found:
            return

        for name, alias in node.names:
            if name == ("pandas" or "tensor"):
                self.has_import = True

    def visit_for(self, node: astroid.For) -> None:
        if self.code_smell_found or self.has_import is False:
            return

        if self.dfs(node=node.iter):
            # Code smell
            self.record_finding(node=node)
            self.code_smell_found = True

    def visit_while(self, node: astroid.While) -> None:
        if self.code_smell_found or self.has_import is False:
            return

        if self.dfs(node=node.test):
            # Code smell
            self.record_finding(node=node)
            self.code_smell_found = True

    def dfs(self, node: astroid.NodeNG) -> bool:
        if hasattr(node, 'infer'):
            try:
                for inferred in node.inferred():
                    if "tensorflow" in str(inferred) or "pandas" in str(inferred):
                        return True
            except astroid.InferenceError:
                pass

        for child in node.get_children():
            if self.dfs(child):  # recursively call dfs on the child
                return True
        return False

    def record_finding(self, node: astroid.NodeNG) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Unnecessary Iteration",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="Avoid unnecessary iterations. Use vectorized solutions instead of loops.",
                             pipeline_stage="Data Cleaning",
                             effect="Efficiency",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
