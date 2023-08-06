import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class PytorchCallMethodMisused(BaseChecker):
    """
    This class is devised to detect instances where self.net.forward() is improperly used instead of the suggested
    self.net() in PyTorch code. It begins by scrutinizing for the attribute forward that is a child of a self.net
    call, a pattern indicating the incorrect use of self.net.forward().
    """

    ID = "CS19"
    TITLE = "Use self.net() in PyTorch to forward the input to the network instead of self.net.forward()."
    DESCRIPTION = """
    Context:
    Both self.net() and self.net.forward() can be used to forward
    the input into the network in PyTorch.

    Problem:
    In PyTorch, self.net() and self.net.forward() are not identical.
    The self.net() also deals with all the register hooks, which would
    not be considered when calling the plain .forward().

    Solution:
    It is recommended to use self.net() rather than
    self.net.forward().
    """

    def __init__(self, filename):
        super().__init__(filename)

    def visit_attribute(self, node: astroid.Attribute):
        # Check if the attribute is 'forward' and its parent is a call to 'self.net'
        if node.attrname == 'forward' and isinstance(node.expr, astroid.Attribute):
            if (
                    node.expr.attrname == 'net' and
                    isinstance(node.expr.expr, astroid.Name) and
                    node.expr.expr.name == 'self'
            ):
                self.record_finding(node=node)

    def record_finding(self, node: astroid.Attribute) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Pytorch Call Method Misused",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="API-Specific: PyTorch",
                             description="Use self.net() in PyTorch to forward the input to the network instead of "
                                         "self.net.forward().",
                             pipeline_stage="Model Training",
                             effect="Robustness",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
