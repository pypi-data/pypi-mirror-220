import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class ColumnsAndDataTypeNotExplicitlySet(BaseChecker):
    """
    This class checks function calls for the inferred "pandas" module and the presence of attribute names beginning
    with "read_". It also inspects for the explicit use of keyword arguments "columns" and "dtype" within these
    "read_" method calls.
    """

    ID = "CS4"
    TITLE = "Explicitly select columns and set DataType when importing data."
    DESCRIPTION = """
    Context:
    In Pandas, all columns are selected by default when a
    DataFrame is imported from a file or other sources. The data type
    for each column is defined based on the default dtype conversion.

    Problem:
    If the columns are not selected explicitly, it is not easy
    for developers to know what to expect in the downstream data
    schema. If the datatype is not set explicitly, it may silently
    continue the next step even though the input is unexpected, which
    may cause errors later. The same applies to other data importing
    scenarios.

    Solution:
    It is recommended to set the columns and DataType explicitly in data processing.
    """

    def __init__(self, filename):
        super().__init__(filename)

    def visit_call(self, node: astroid.nodes.Call):
        has_pandas_module = False

        if (
                isinstance(node.func, astroid.Attribute)
                and isinstance(node.func.expr, astroid.Name)
                and node.func.attrname.startswith('read_')
        ):
            for inferred in node.func.expr.inferred():
                if isinstance(inferred, astroid.Module) and "pandas" in inferred.name:
                    has_pandas_module = True
                elif "pandas" in str(inferred):
                    has_pandas_module = True

        if has_pandas_module:
            self.check_explicit_columns_and_dtype(node=node)

    def check_explicit_columns_and_dtype(self, node: astroid.Call):
        explicit_columns = False
        explicit_dtype = False

        for keyword in node.keywords:
            if keyword.arg == 'usecols':
                explicit_columns = True

            if keyword.arg == 'dtype':
                explicit_dtype = True

        if not explicit_columns or not explicit_dtype:
            self.record_finding(node=node)

    def record_finding(self, node: astroid.Call) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Columns and DataType Not Explicitly Set",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Error-prone",
                             description="Explicitly select columns and set DataType when importing data.",
                             pipeline_stage="Data Cleaning",
                             effect="Readability",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
