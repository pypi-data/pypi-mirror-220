import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class DataframeConversionAPIMisused(BaseChecker):
    """
    This class verifies whether a node is an Attribute with the name "values", if the expression of the attribute is
    a Name node, and if this expression infers to a pandas DataFrame instance.
    References: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.values.html
    """

    ID = "CS8"
    TITLE = "Use df.to_numpy() in Pandas instead of df.values() for transform a DataFrame to a NumPy array."
    DESCRIPTION = """
    Context:
    In Pandas, df.to_numpy() and df.values() both can turn a
    DataFrame to a NumPy array.

    Problem:
    As noted in, df.values() has an inconsistency problem.
    With .values() it is unclear whether the returned value would be the
    actual array, some transformation of it, or one of the Pandas custom
    arrays. However, the .values() API has not been not deprecated
    yet. Although the library developers note it as a warning in the
    documentation, it does not log a warning or error when compiling
    the code if we use .value().

    Solution:
    When converting DataFrame to NumPy array, it is better
    to use df.to_numpy() than df.values().
    """

    def __init__(self, filename):
        super().__init__(filename)

    def visit_attribute(self, node):
        if isinstance(node, astroid.Attribute) and node.attrname == "values":
            if isinstance(node.expr, astroid.Name):
                for inferred in node.expr.inferred():
                    if isinstance(inferred, astroid.Instance) and inferred.pytype() == "pandas.core.frame.DataFrame":
                        self.record_finding(node=node)

    def record_finding(self, node: astroid.Attribute) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Dataframe Conversion API Misused",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="API-Specific: Pandas",
                             description="Use df.to_numpy() in Pandas instead of df.values() for transform a "
                                         "DataFrame to a NumPy array.",
                             pipeline_stage="Data Cleaning",
                             effect="Error-prone",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
