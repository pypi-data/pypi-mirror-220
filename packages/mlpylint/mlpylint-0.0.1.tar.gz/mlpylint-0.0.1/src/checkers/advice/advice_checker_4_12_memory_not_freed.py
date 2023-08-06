import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class MemoryNotFreed(BaseChecker):
    """
    This class inspects the Python code for import statements related to the "tensorflow" or "pytorch" libraries.
    """

    ID = "CSA12"
    TITLE = "Free memory in time."
    DESCRIPTION = """
    Context:
    Machine learning training is memory-consuming, and
    the machine’s memory is always limited by budget.

    Problem:
    If the machine runs out of memory while training the
    model, the training will fail.

    Solution:
    Some APIs are provided to alleviate the run-out-ofmemory
    issue in deep learning libraries. TensorFlow’s documentation
    notes that if the model is created in a loop, it is suggested to use
    clear_session() in the loop. Meanwhile, the GitHub repository
    pytorch-styleguide recommends using .detach() to free the tensor
    from the graph whenever possible. The .detach() API can prevent
    unnecessary operations from being recorded and therefore can save
    memory. Developers should check whether they use this kind
    of APIs to free the memory whenever possible in their code.
    """

    def __init__(self, filename):
        super().__init__(filename)

    def visit_import(self, node: astroid.Import) -> None:
        for name, alias in node.names:
            if name == "tensorflow":
                self.record_finding(node=node)

            if name == "torch":
                self.record_finding(node=node)

    def record_finding(self, node: astroid.Import) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Memory Not Freed",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="Free memory in time.",
                             pipeline_stage="Model Training",
                             effect="Memory Issue",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
