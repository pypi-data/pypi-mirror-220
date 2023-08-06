import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class BroadcastingFeatureNotUsed(BaseChecker):
    """
    This class scrutinizes the Python code for import statements pertaining to the "pytorch" or "tensorflow" libraries.
    """

    ID = "CSA16"
    TITLE = "Use the broadcasting feature in deep learning code to be more memory efficient."
    DESCRIPTION = """
    Context:
    Deep learning libraries like PyTorch and TensorFlow supports
    the element-wise broadcasting operation.

    Problem:
    Without broadcasting, tiling a tensor first to match another
    tensor consumes more memory due to the creation and storage
    of a middle tiling operation result.

    Solution:
    With broadcasting, it is more memory efficient. However,
    there is a trade-off in debugging since the tiling process is not
    explicitly stated.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.has_import = False

    def visit_import(self, node: astroid.Import) -> None:
        if self.has_import:
            return

        for name, alias in node.names:
            if name == ("torch" or "tensorflow"):
                self.has_import = True
                self.record_finding(node=node)

    def visit_importfrom(self, node: astroid.ImportFrom) -> None:
        if self.has_import:
            return

        if node.modname == ("torch" or "tensorflow"):
            self.has_import = True

    def record_finding(self, node: astroid.NodeNG) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Broadcasting Feature Not Used",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="Use the broadcasting feature in deep learning code to be more memory "
                                         "efficient.",
                             pipeline_stage="Model Training",
                             effect="Efficiency",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
