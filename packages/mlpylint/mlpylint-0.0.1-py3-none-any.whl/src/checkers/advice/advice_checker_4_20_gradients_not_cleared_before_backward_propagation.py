import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class GradientsNotClearedBeforeBackwardPropagation(BaseChecker):
    """
    This class inspects the Python code for the import of "torch" and reviews function calls to verify the presence
    of the attributes "zero_grad", "backward", or "step". It also checks whether the inferred string within these
    calls contains "torch".
    """

    ID = "CSA20"
    TITLE = "Use optimizer.zero_grad(), loss_fn.backward(), optimizer.step() together in order in PyTorch. Do not " \
            "forget to use optimizer.zero_grad() before loss_fn.backward() to clear gradients. "
    DESCRIPTION = """
    Context:
    In PyTorch, optimizer.zero_grad() clears the old gradients
    from last step, loss_fn.backward() does the back propagation, and
    optimizer.step() performs weight update using the gradients.

    Problem:
    If optimizer.zero_grad() is not used before loss_fn.backward(),
    the gradients will be accumulated from all loss_fn.backward()
    calls, and it will lead to the gradient explosion, which
    fails the training.

    Solution:
    Developers should use optimizer.zero_grad(), loss_fn.backward(),
    optimizer.step() together in order and should not forget to use
    optimizer.zero_grad() before loss_fn.backward().
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.has_torch_import = False
        self.code_smell_found = False

    def visit_import(self, node: astroid.Import) -> None:
        for name, alias in node.names:
            if name == "torch":
                self.has_torch_import = True

    def visit_call(self, node: astroid.Call):
        if self.code_smell_found:
            return

        if (
                self.has_torch_import
                and isinstance(node.func, astroid.Attribute)
                and node.func.attrname in {"zero_grad", "backward", "step"}
                and any("torch" in str(infer) for infer in node.func.inferred())
        ):
            self.code_smell_found = True
            self.record_finding(node=node)

    def record_finding(self, node: astroid.Call) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Gradients Not Cleared before Backward Propagation",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="API-Specific: PyTorch",
                             description="Use optimizer.zero_grad(), loss_fn.backward(), optimizer.step() together in "
                                         "order in PyTorch. Do not forget to use optimizer.zero_grad() before "
                                         "loss_fn.backward() to clear gradients.",
                             pipeline_stage="Model Training",
                             effect="Error-prone",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
