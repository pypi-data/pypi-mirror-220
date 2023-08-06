import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class TensorArrayNotUsed(BaseChecker):
    """
    This class verifies the import of 'tensorflow' in Python code. It checks for the initialization of an array using
    'tf.constant()' and inspects whether there is an attempt to assign a new value to this array inside a loop,
    which could lead to an error.
    """

    ID = "CS17"
    TITLE = "Use tf.TensorArray() in TensorFlow 2 if the value of the array will change in the loop."
    DESCRIPTION = """
    Context:
    Developers may need to change the value of the array in
    the loops in TensorFlow.

    Problem:
    If the developer initializes an array using tf.constant()
    and tries to assign a new value to it in the loop to keep it growing,
    the code will run into an error. The developer can fix this error
    by the low-level tf.while_loop() API. However, it is inefficient
    coding in this way. A lot of intermediate tensors are built in this
    process.

    Solution:
    Using tf.TensorArray() for growing array in the loop is a
    better alternative for this kind of problem in TensorFlow 2. Developers
    should use new data types from libraries for more intelligent
    solutions.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.tensorflow_alias = set()
        self.tensorflow_constants = set()

    def visit_import(self, node: astroid.Import) -> None:
        for name, alias in node.names:
            if name == "tensorflow":
                if node.names[0][1] is not None:
                    self.tensorflow_alias.add(node.names[0][1])
                else:
                    self.tensorflow_alias.add(node.names[0][0])

    def visit_assign(self, node: astroid.Assign):
        if (
                isinstance(node.value, astroid.Call) and
                isinstance(node.value.func, astroid.Attribute) and
                node.value.func.attrname == 'constant' and
                isinstance(node.value.func.expr, astroid.Name) and
                node.value.func.expr.name in self.tensorflow_alias
        ):
            if isinstance(node.targets[0], astroid.AssignName):
                self.tensorflow_constants.add(node.targets[0].name)

    def visit_augassign(self, node: astroid.AugAssign):
        if (
                isinstance(node.parent, (astroid.For, astroid.While)) and
                isinstance(node.target, astroid.AssignName) and
                node.target.name in self.tensorflow_constants
        ):
            self.record_finding(node=node)

    def record_finding(self, node: astroid.AugAssign) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="TensorArray Not Used",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="API-Specific: TensorFlow 2",
                             description="Use tf.TensorArray() in TensorFlow 2 if the value of the array will change "
                                         "in the loop.",
                             pipeline_stage="Model Training",
                             effect="Efficiency & Error-prone",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
