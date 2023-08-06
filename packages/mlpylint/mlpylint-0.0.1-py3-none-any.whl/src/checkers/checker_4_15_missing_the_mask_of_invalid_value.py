import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class MissingTheMaskOfInvalidValue(BaseChecker):
    """
    This class requires the use of 'TensorFlow v2.x' and checks for its import in the Python code. It searches for
    calls to the 'math.log' function and verifies whether the argument for 'tf.log()' is encapsulated with
    'tf.clip_by_value()' to prevent issues with the argument turning to zero. If the 'clip_by_value' function or
    argument 'x' through 'clip_by_value' is not used, these are identified as potential code smells.
    References: https://www.tensorflow.org/api_docs/python/tf/math/log
    """

    ID = "CS15"
    TITLE = "Add a mask for possible invalid values. For example, developers should wrap the argument for tf.log() " \
            "with tf.clip() to avoid the argument turning to zero. "
    DESCRIPTION = """
    Context:
    In deep learning, the value of the variable changes during
    training. The variable may turn into an invalid value for another
    operation in this process.

    Problem:
    Several posts on Stack Overflow talk about the pitfalls
    that are not easy to discover caused by the input of the log function
    approaching zero. In this kind of programs, the input variable turns to
    zero and becomes an invalid value for tf.log(), which raises an error
    during the training process. However, the error’s stack trace did not
    directly point to the line of code that the bug exists.
    This problem is not easy to debug and may take a long training time to find.

    Solution:
    The developer should check the input for the log function
    or other functions that have special requirements for the argument
    and add a mask for them to avoid the invalid value. For example,
    developer can change tf.log(x) to tf.log(tf.clip_by_value(x,1e-10,1.0)).
    If the value of x becomes zero, i.e., lower than the lowest bound
    1e-10, the tf.clip_by_value() API will act as a mask and outputs
    1e-10. It will save time and effort if the developer could identify
    this smell before the code run into errors.

    
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.tensorflow_alias = set()

    def visit_import(self, node: astroid.Import):
        for name, alias in node.names:
            if name == "tensorflow":
                if node.names[0][1] is not None:
                    self.tensorflow_alias.add(node.names[0][1])
                else:
                    self.tensorflow_alias.add(node.names[0][0])

    def visit_call(self, node: astroid.Call):
        if isinstance(node.func, astroid.Attribute) and node.func.attrname == "log":
            if (
                    isinstance(node.func.expr, astroid.Attribute)
                    and isinstance(node.func.expr.expr, astroid.Name)
                    and node.func.expr.expr.name in self.tensorflow_alias
                    and node.func.expr.attrname == "math"
            ):
                self.missing_the_mask_of_invalid_value(node=node)

    def missing_the_mask_of_invalid_value(self, node: astroid.Call):
        # Check if keyword x is missing the mask of invalid value
        x_found = False
        if node.keywords:
            for key in node.keywords:
                if key.arg == "x":
                    x_found = True
                    if (
                            not isinstance(key.value, astroid.Call)
                    ) or (
                            isinstance(key.value, astroid.Call)
                            and isinstance(key.value.func, astroid.Attribute)
                            and key.value.func.attrname != "clip_by_value"
                    ):
                        # Code smell - tf.clip_by_value call is not used for x keyword
                        self.record_finding(node=node)
                        return

        # Check if argument is missing the mask of invalid value
        if (
                not x_found
                and node.args
                and not isinstance(node.args[0], astroid.Call)
        ) or (
                node.args
                and isinstance(node.args[0], astroid.Call)
                and isinstance(node.args[0].func, astroid.Attribute)
                and node.args[0].func.attrname != "clip_by_value"
        ):
            # Code smell - tf.clip_by_value call is not used
            self.record_finding(node=node)

    def record_finding(self, node: astroid.Call) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Missing the Mask of Invalid Value",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="Add a mask for possible invalid values. For example, developers should wrap "
                                         "the argument for tf.log() with tf.clip() to avoid the argument turning to "
                                         "zero.",
                             pipeline_stage="Model Training",
                             effect="Error-prone",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
