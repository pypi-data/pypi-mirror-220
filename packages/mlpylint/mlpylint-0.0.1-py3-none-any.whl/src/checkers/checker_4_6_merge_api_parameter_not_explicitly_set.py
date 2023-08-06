import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class MergeAPIParameterNotExplicitlySet(BaseChecker):
    """
    This class verifies whether a function call named "merge" pertains to the pandas DataFrame pytype. Additionally,
    it checks if the parameters {'on', 'how', 'validate'} are set within these function calls.
    """

    ID = "CS6"
    TITLE = "Explicitly specify the parameters for merge operations. Specifically, explicitly specify on, " \
            "how and validate parameter for df.merge() API in Pandas for better readability. "
    DESCRIPTION = """
    Context:
    df.merge() API merges two DataFrames in Pandas.

    Problem:
    Although using the default parameter can produce the
    same result, explicitly specify on and how produce better readability.
    The parameter on states which columns to join on, and the
    parameter how describes the join method (e.g., outer, inner). Also,
    the validate parameter will check whether the merge is of a specified
    type. If the developer assumes the merge keys are unique in
    both left and right datasets, but that is not the case, and he does
    not specify this parameter, the result might silently go wrong. The
    merge operation is usually computationally and memory expensive.
    It is preferable to do the merging process in one stroke for
    performance consideration.

    Solution:
    Developer should explicitly specify the parameters for merge operation.
    """

    def __init__(self, filename):
        super().__init__(filename)

    def visit_call(self, node: astroid.Call):
        if isinstance(node.func, astroid.Attribute) and node.func.attrname == 'merge':
            # Check inferred object is of type "pandas"
            if hasattr(node.func.expr, "infer"):
                for inferred in node.func.expr.inferred():
                    if (
                            isinstance(inferred, astroid.Instance)
                            and inferred.pytype() == "pandas.core.frame.DataFrame"
                    ):
                        self.check_merge_call(node)

    def check_merge_call(self, node: astroid.Call):
        required_params = {'on', 'how', 'validate'}

        # Iterate through keyword arguments of the merge() call
        for kwarg in node.keywords:
            # If the keyword argument name is in the required_params set, remove it
            if kwarg.arg in required_params:
                required_params.remove(kwarg.arg)

        # If the required_params set is not empty, it means some parameters were not explicitly specified
        if required_params:
            self.record_finding(node=node)

    def record_finding(self, node: astroid.Call) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Merge API Parameter Not Explicitly Set",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="explicitly specify on, how and validate parameter for df.merge() API in "
                                         "Pandas for better readability.",
                             pipeline_stage="Data Cleaning",
                             effect="Readability & Error-prone",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
