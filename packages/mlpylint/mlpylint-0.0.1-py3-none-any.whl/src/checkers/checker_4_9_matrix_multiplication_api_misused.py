import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class MatrixMultiplicationAPIMisused(BaseChecker):
    """
    This class performs several checks involving the usage of the "numpy" library:
    - It verifies the import of "numpy", storing its alias for subsequent checks.
    - It checks for assignments of two-dimensional numpy arrays, storing the associated variable names.
    - It scrutinizes function calls for the invocation of the 'dot()' function:
        - If the 'dot()' function is invoked on the numpy alias and its arguments are variables storing two-dimensional
        numpy arrays, this is flagged as a code smell.
    - If any of these checks pass, it records the code smell instance.

    """

    ID = "CS9"
    TITLE = "When the multiply operation is performed on two-dimensional matrixes, use np.matmul() instead of " \
            "np.dot() in NumPy for better semantics."
    DESCRIPTION = """
    Context:
    When the multiply operation is performed on twodimensional
    matrixes, np.matmul() and np.dot() give the same result,
    which is a matrix.

    Problem:
    In mathematics, the result of the dot product is expected
    to be a scalar rather than a vector. The np.dot() returns a new
    matrix for two-dimensional matrixes multiplication, which does
    not match with its mathematics semantics. Developers sometimes
    use np.dot() in scenarios where it is not supposed to, e.g., twodimensional
    multiplication.

    Solution:
    When the multiply operation is performed on twodimensional
    matrixes, np.matmul() is preferred over np.dot() for its clear semantic.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.has_numpy_import = False
        self.numpy_alias = set()
        self.two_dim_vals = set()

    def visit_import(self, node: astroid.Import) -> None:
        for name, alias in node.names:
            if name == "numpy":
                self.numpy_alias.add(alias if alias else name)
                self.has_numpy_import = True

    def visit_assign(self, node: astroid.Assign):
        for target in node.targets:
            if isinstance(target, astroid.AssignName) and target.name in self.two_dim_vals:
                self.two_dim_vals.remove(target.name)

        if not isinstance(node.value, astroid.Call):
            return

        if not (self.inferred_ndarray(node) or self.is_numpy_array(node)):
            return

        arg_value = node.value.args[0] if (node.value.args and isinstance(node.value.args[0], astroid.List)) else None

        if arg_value and self.is_2d_array(arg_value) and isinstance(node.targets[0], astroid.AssignName):
            self.two_dim_vals.add(node.targets[0].name)

    def visit_call(self, node: astroid.Call):
        if (
                isinstance(node.func, astroid.Attribute)
                and node.func.attrname == "dot"
                and isinstance(node.func.expr, astroid.Name)
                and node.func.expr.name in self.numpy_alias
                and len(node.args) == 2
                and isinstance(node.args[0], astroid.Name)
                and isinstance(node.args[1], astroid.Name)
                and node.args[0].name in self.two_dim_vals
                and node.args[1].name in self.two_dim_vals
        ):
            self.record_finding(node=node)

    @staticmethod
    def inferred_ndarray(node) -> bool:
        try:
            return any(
                isinstance(infer, astroid.Instance)
                and infer.pytype() == ".ndarray"
                for infer in node.value.inferred()
            )
        except astroid.exceptions.InferenceError:
            return False

    def is_numpy_array(self, node) -> bool:
        if not isinstance(node.value.func, astroid.Attribute):
            return False
        if not isinstance(node.value.func.expr, astroid.Name):
            return False
        if node.value.func.expr.name not in self.numpy_alias:
            return False
        if node.value.func.attrname != "array":
            return False
        return True

    @staticmethod
    def is_2d_array(arg_value: astroid.List) -> bool:
        if len(arg_value.elts) != 2:
            return False

        inner_list_1 = arg_value.elts[0] if isinstance(arg_value.elts[0], astroid.List) else None
        inner_list_2 = arg_value.elts[1] if isinstance(arg_value.elts[1], astroid.List) else None

        return all([
            inner_list is not None and len(inner_list.elts) == 2
            for inner_list in [inner_list_1, inner_list_2]
        ]) and all([
            isinstance(elt, astroid.Const) and isinstance(elt.value, (float, int))
            for inner_list in [inner_list_1, inner_list_2] if inner_list is not None
            for elt in inner_list.elts
        ])

    def record_finding(self, node: astroid.Call) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Matrix Multiplication API Misused",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="API-Specific: NumPy",
                             description="When the multiply operation is performed on two-dimensional matrixes, "
                                         "use np.matmul() instead of np.dot() in NumPy for better semantics.",
                             pipeline_stage="Data Cleaning",
                             effect="Readability",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
