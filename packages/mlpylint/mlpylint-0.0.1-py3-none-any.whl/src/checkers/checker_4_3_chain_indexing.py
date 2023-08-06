import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker

COMPARISON_OP = frozenset(("<", "<=", ">", ">=", "!=", "==", "is", "is not"))  # Note: python 3.10 does not support "<>"


class ChainIndexing(BaseChecker):
    """
    This class verifies the import of "pandas" in Python code and stores its alias. It also examines inferred strings
    associated with 'pandas' for subscript operations and ensures that the parent node is of the same subscript type.
    """

    ID = "CS3"
    TITLE = "Avoid using chain indexing in Pandas."
    DESCRIPTION = """
    Context:
    In Pandas, df[“one”][“two”] and df.loc[:,(“one”,“two”)] give
    the same result. df[“one”][“two”] is called chain indexing.

    Problem:
    Using chain indexing may cause performance issues as
    well as error-prone code. For example, when using
    df[“one”][“two”], Pandas sees this operation as two events: call
    df[“one”] first and call [“two”] based on the result the previous
    operation gets. On the contrary, df.loc[:,(“one”,“two”)] only performs
    a single call. In this way, the second approach can be significantly
    faster than the first one. Furthermore, assigning to the product of
    chain indexing has inherently unpredictable results. Since Pandas
    makes no guarantees on whether df[“one”] will return a view or a
    copy, the assignment may fail.

    Solution:
    Developers using Pandas should avoid using chain indexing
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.has_pandas_import = False
        self.pandas_alias = set()

    def visit_import(self, node: astroid.Import) -> None:
        for name, alias in node.names:
            if name == "pandas":
                if alias is not None:
                    self.pandas_alias.add(alias)
                else:
                    self.pandas_alias.add(name)

            self.has_pandas_import = True

    def visit_subscript(self, node: astroid.Subscript):
        if not self.has_pandas_import:
            return

        if isinstance(node.value, astroid.Name):
            for inferred in node.value.inferred():
                if (
                        "pandas" in str(inferred)
                        and hasattr(node, "parent")
                        and isinstance(node.parent, astroid.Subscript)
                ):
                    self.record_finding(node=node)

    def record_finding(self, node: astroid.Subscript) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Chain Indexing",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="API-Specific: Pandas",
                             description="Avoid using chain indexing in Pandas.",
                             pipeline_stage="Data Cleaning",
                             effect="Error-prone",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
