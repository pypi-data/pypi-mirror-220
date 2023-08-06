import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class DataLeakage(BaseChecker):
    """
    This class checks whether "Sklearn" is imported or used within 'importfrom' statements and verifies if
    'sklearn.pipeline.Pipeline' is utilized in the code. If not, it identifies and records this as a potential code
    smell.
    """

    ID = "CSA21"
    TITLE = "Use Pipeline() API in Scikit-Learn or check data segregation carefully when using other libraries to " \
            "prevent data leakage."
    DESCRIPTION = """
    Context:
    The data leakage occurs when the data used for training a
    machine learning model contains prediction result information.

    Problem:
    Data leakage frequently leads to overly optimistic experimental
    outcomes and poor performance in real-world usage.

    Solution:
    There are two main sources of data leakage: leaky predictors
    and a leaky validation strategy. Leaky predictors are
    the cases in which some features used in training are modified or
    generated after the goal value has been achieved. This kind of data
    leakage can only be inspected at the data level rather than the code
    level. Leaky validation strategy refers to the scenario where training
    data is mixed with validation data. This fault can be checked
    at the code level. One best practice in Scikit-Learn is to use the
    Pipeline() API to prevent data leakage.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.has_sklearn_import = False
        self.has_sklearn_pipeline = False
        self.sklearn_node = None

    def visit_nodes(self, node: astroid.NodeNG) -> None:
        if isinstance(node, astroid.Import):
            for name, alias in node.names:
                if "sklearn" in name:
                    self.sklearn_node = node
                    self.has_sklearn_import = True
        elif (
                isinstance(node, astroid.ImportFrom)
                and "sklearn" in node.modname
        ):
            self.has_sklearn_import = True
            self.sklearn_node = node

            if "Pipeline" in node.names[0]:
                # Checks if Pipeline is imported directly "from sklearn.pipeline import Pipeline"
                # Assuming that it is being used
                self.has_sklearn_pipeline = True
        elif (
                isinstance(node, astroid.Call)
        ):
            if (
                    isinstance(node.func, astroid.Attribute)
                    and node.func.attrname == "Pipeline"
                    and isinstance(node.func.expr, astroid.Attribute)
                    and node.func.expr.attrname == "pipeline"
            ):
                for infer in node.func.expr.inferred():
                    if "sklearn" in str(infer):
                        self.has_sklearn_pipeline = True

        for child in node.get_children():
            self.visit_nodes(child)

    def visit_module(self, module_node: astroid.Module) -> None:
        # Iterate module and search for indicators
        for node in module_node.body:
            self.visit_nodes(node=node)

        if self.has_sklearn_import and not self.has_sklearn_pipeline:
            self.record_finding(node=self.sklearn_node)

    def record_finding(self, node: astroid.NodeNG) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Data Leakage",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="Use Pipeline() API in Scikit-Learn or check data segregation carefully when "
                                         "using other libraries to prevent data leakage.",
                             pipeline_stage="Model Evaluation",
                             effect="Error-prone",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
