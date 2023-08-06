import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class InPlaceAPIsMisused(BaseChecker):
    """
    This class inspects whether the value of an expression is a function call, originating either from a pandas
    DataFrame instance or the numpy module. It checks if the function invoked is "dropna" or "clip", and ensures that
    the "inplace" parameter is not set to True.
    """

    ID = "CS7"
    TITLE = "Remember to assign the result of an operation to a variable or set the in-place parameter in the API."
    DESCRIPTION = """
    Context:
    Data structures can be manipulated in mainly two different
    approaches: 1) by applying the changes to a copy of the data
    structure and leaving the original object intact, or 2) by changing
    the existing data structure (also known as in-place).

    Problem:
    Some methods can adopt in-place by default, while others
    return a copy. If the developer assumes an in-place approach,
    he will not assign the returned value to any variable. Hence, the
    operation will be executed, but it will not affect the final outcome.
    For example, when using the Pandas library, the developer may not
    assign the result of df.dropna() to a variable. He may assume that
    this API will make changes on the original DataFrame and not set
    the in-place parameter to be True either. The original DataFrame
    will not be updated in this way [4]. In the “TensorFlow Bugs” replication
    package, we also code_smell_found an example where the developer
    thought np.clip() is an in-place operation and used it without assigning
    it to a new variable.

    Solution:
    We suggest developers check whether the result of the
    operation is assigned to a variable or the in-place parameter is set in
    the API. Some developers hold the view that the in-place operation
    will save memory. However, this is a misconception in the Pandas
    library because the copy of the data is still created. In PyTorch, the
    in-place operation does save GPU memory, but it risks overwriting
    the values needed to compute the gradient.
    """

    def __init__(self, filename):
        super().__init__(filename)

    def visit_expr(self, node: astroid.Expr):
        if isinstance(node.value, astroid.Call):
            if self.check_in_place_api_misuse(node.value):
                self.record_finding(node=node)

    @staticmethod
    def check_in_place_api_misuse(call: astroid.Call) -> bool:
        if not isinstance(call.func, astroid.Attribute):
            return False

        if isinstance(call.func.expr, astroid.Name) and hasattr(call.func.expr, "infer"):
            for inferred in call.func.expr.inferred():
                if (
                        (isinstance(inferred, astroid.Instance) and inferred.pytype() == "pandas.core.frame.DataFrame")
                        or (isinstance(inferred, astroid.Module) and inferred.name == "numpy")
                ):
                    if call.func.attrname in {"dropna", "clip"}:
                        return not any(
                            kwarg.arg == "inplace" and kwarg.value.as_string() == "True" for kwarg in call.keywords)

        return False

    def record_finding(self, node: astroid.Expr) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="In-Place APIs Misused",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="Remember to assign the result of an operation to a variable or set the "
                                         "in-place parameter in the API.",
                             pipeline_stage="Data Cleaning",
                             effect="Error-prone",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
