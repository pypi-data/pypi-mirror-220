import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class TrainingAndEvaluationModeImproperToggling(BaseChecker):
    """
    This class is designed to validate and keep track of the import of "torch" along with its alias, scrutinize
    'importfrom' statements related to "torch" to see if "eval" is being imported, and, provided that "torch" is
    imported, assess function calls for instances of 'torch.eval' usage.
    """

    ID = "CSA18"
    TITLE = "Call the training mode in the appropriate place in deep learning code to avoid forgetting to toggle back " \
            "the training mode after the inference step. "
    DESCRIPTION = """
    Context:
    In PyTorch, calling .eval() means we are going into the
    evaluation mode and the Dropout layer will be deactivated.

    Problem:
    If the training mode did not toggle back in time, the
    Dropout layer would not be used in some data training and thus
    affect the training result. The same applies to TensorFlow library.

    Solution:
    Developers should call the training mode in the right
    place to avoid forgetting to switch back to the training mode after
    the inference step.
    """

    def __init__(self, filename):
        super().__init__(filename)

        self.has_torch_import = False
        self.torch_alias = set()
        self.code_smell_found = False

    def visit_import(self, node: astroid.Import) -> None:
        if self.code_smell_found:
            return

        for name, alias in node.names:
            if name == "torch":
                if node.names[0][1] is not None:
                    self.torch_alias.add(node.names[0][1])
                else:
                    self.torch_alias.add(node.names[0][0])

                self.has_torch_import = True

    def visit_importfrom(self, node: astroid.ImportFrom) -> None:
        if self.code_smell_found:
            return

        if node.modname == "torch":
            if "eval" in node.names[0]:
                self.record_finding(node=node)
                self.code_smell_found = True

    def visit_call(self, node: astroid.Call) -> None:
        if self.code_smell_found:
            return

        if (
                self.has_torch_import and
                isinstance(node.func, astroid.Attribute) and
                node.func.attrname == "eval"
        ):
            for infer in node.func.inferred():
                if "torch" in str(infer):
                    self.record_finding(node=node)
                    self.code_smell_found = True

    def record_finding(self, node: astroid.NodeNG) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Training / Evaluation Mode Improper Toggling",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="Call the training mode in the appropriate place in deep learning code to "
                                         "avoid forgetting to toggle back the training mode after the inference step.",
                             pipeline_stage="Model Training",
                             effect="Error-prone",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
