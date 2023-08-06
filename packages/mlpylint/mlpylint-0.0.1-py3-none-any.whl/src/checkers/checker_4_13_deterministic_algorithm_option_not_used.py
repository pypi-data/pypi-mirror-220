import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class DeterministicAlgorithmOptionNotUsed(BaseChecker):
    """
    This class verifies the import of 'pytorch' in Python code and checks whether
    'torch.use_deterministic_algorithms' is invoked without any arguments being passed.
    """

    ID = "CS13"
    TITLE = "Set deterministic algorithm option to True during the development process, and use the option that " \
            "provides better performance in the production. "
    DESCRIPTION = """
    Context:
    Using deterministic algorithms can improve reproducibility.

    Problem:
    The non-deterministic algorithm cannot produce repeatable
    results, which is inconvenient for debugging.

    Solution:
    Some libraries provide APIs for developers to use the
    deterministic algorithm. In PyTorch, it is suggested to set torch.use_-
    deterministic_algorithms(True) when debugging. However, the
    application will perform slower if this option is set, so it is suggested
    not to use it in the deployment stage.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.torch_alias = set()
        self.has_use_deterministic_algorithms = False

    def visit_import(self, node: astroid.Import) -> None:
        for name, alias in node.names:
            if name == "torch":
                self.torch_alias.add(alias if alias else name)

    def visit_call(self, node: astroid.Call):
        # Check if this is a call to torch.use_deterministic_algorithms
        if (
                isinstance(node.func, astroid.Attribute)
                and node.func.attrname == "use_deterministic_algorithms"
                and isinstance(node.func.expr, astroid.Name)
                and node.func.expr.name in self.torch_alias
        ):
            if node.args and isinstance(node.args[0], astroid.Const):
                # Check if argument is set to true
                if isinstance(node.args[0].value, bool):
                    if node.args[0].value is True:
                        self.has_use_deterministic_algorithms = True
                    elif node.args[0].value is False:
                        self.record_finding(node=node)
            elif node.keywords:
                for key in node.keywords:
                    if (
                            key.arg == "mode"
                            and isinstance(key.value, astroid.Const)
                            and isinstance(key.value.value, bool)
                    ):
                        if key.value.value is False:
                            self.record_finding(node=node)

    def leave_module(self, node: astroid.Module):
        if self.has_use_deterministic_algorithms:
            self.record_finding(node=node)

    def record_finding(self, node: astroid.NodeNG) -> None:
        Result.add(
            CodeSmell(
                code_smell_id="CS13",
                code_smell_title="Deterministic Algorithm Option Not Used",
                file_path=self.filename,
                line=node.lineno,
                col_offset=node.col_offset,
                smell_type="Generic",
                description="Set deterministic algorithm option to True during the development process, "
                            "and use the option that provides better performance in the production.",
                pipeline_stage="Model Training",
                effect="Reproducibility",
                source_code=node.as_string(),
                source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}",
            )
        )