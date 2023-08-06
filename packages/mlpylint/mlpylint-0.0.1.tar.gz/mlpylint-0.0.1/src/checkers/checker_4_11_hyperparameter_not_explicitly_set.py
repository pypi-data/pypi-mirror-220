import astroid
from astroid.helpers import safe_infer

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class HyperparameterNotExplicitlySet(BaseChecker):
    """
    This class examines the setting of hyperparameters for machine learning models, specifically focusing on the
    'KMeans' algorithm from the 'sklearn' library and the 'SGD' optimizer from the 'torch' library.
    """

    ID = "CS11"
    TITLE = "Hyperparameters should be set explicitly."
    DESCRIPTION = """
    Context:
    Hyperparameters are usually set before the actual learning
    process begins and control the learning process. These parameters
    directly influence the behavior of the training algorithm
    and therefore have a significant impact on the model’s performance.

    Problem:
    The default parameters of learning algorithm APIs may
    not be optimal for a given data or problem, and may lead to local optima. 
    In addition, while the default parameters of a machine learning
    library may be adequate for some time, these default parameters
    may change in new versions of the library. Furthermore, not setting
    the hyperparameters explicitly is inconvenient for replicating the
    model in a different programming language.

    Solution:
    Hyperparameters should be set explicitly and tuned for
    improving the result’s quality and reproducibility.
    """

    def __init__(self, filename):
        super().__init__(filename)

    def visit_call(self, node: astroid.Call) -> None:
        # Scikit-Learn
        self.check_hyperparam_kmeans_sklearn(node)

        # PyTorch
        self.check_hyperparam_sgd_torch(node)

    def check_hyperparam_kmeans_sklearn(self, node: astroid.Call) -> None:
        inferred_node = safe_infer(node)
        if (
                inferred_node is not None
                and isinstance(inferred_node, astroid.Instance)
                and inferred_node.qname() == "sklearn.cluster._kmeans.KMeans"
        ):
            required_args = ['n_clusters', 'random_state']
            provided_args = [keyword.arg for keyword in node.keywords]
            if not all(arg in provided_args for arg in required_args):
                self.record_finding(node)

    def check_hyperparam_sgd_torch(self, node: astroid.Call) -> None:
        inferred_node = safe_infer(node)
        if (
                inferred_node is not None
                and isinstance(inferred_node, astroid.Instance)
                and inferred_node.qname() == "torch.optim.sgd.SGD"
        ):
            required_args = ['lr', 'momentum', 'weight_decay']
            provided_args = [keyword.arg for keyword in node.keywords]
            if not all(arg in provided_args for arg in required_args):
                self.record_finding(node)

    def record_finding(self, node: astroid.Call) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Hyperparameter Not Explicitly Set",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="Hyperparameters should be set explicitly.",
                             pipeline_stage="Model Training",
                             effect="Error-prone & Reproducibility",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
