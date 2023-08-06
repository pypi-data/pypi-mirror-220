import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class RandomnessUncontrolled(BaseChecker):
    """
    This class performs an extensive review of the Python file to detect any instances of uncontrolled randomness. It
    takes note of 'Scikit-learn's reliance on 'NumPy's random number generator. It seeks out all invocations of
    'numpy.random', 'torch.rand', and Python's 'random.random' that do not have corresponding seed set calls. In
    addition, it focuses on specific scenarios:
    1. The use of 'Scikit-learn's RandomForestClassifier without setting
    the 'random_state' parameter and a global 'NumPy' seed.
    2. The use of 'PyTorch's DataLoader without setting
    'NumPy's manual seed and the 'worker_init_fn' parameter.


    Clarification:
    1. `numpy.random.seed()`: Sets the seed for NumPy's random number generator. Affects any operation relying on NumPy
    for randomness, including Scikit-learn.
    2. `random.seed()`: Sets the seed for Python's built-in random module. Affects Python's native random operations.
    3. `torch.manual_seed()`: Sets the seed for PyTorch's random number generator. Affects PyTorch's random operations.
    4. Scikit-learn relies on NumPy's random number generation. Therefore, setting a seed using `numpy.random.seed()`
    ensures deterministic behavior in Scikit-learn processes.
    """

    ID = "CS14"
    TITLE = "Set random seed explicitly during the development process whenever a possible random procedure is " \
            "involved in the application. "
    DESCRIPTION = """
    Context:
    There are several scenarios involving random seeds. In
    some algorithms, randomness is inherently involved in the training
    process. For the cross-validation process in the model evaluation
    stage, the dataset split by some library APIs can vary depending
    on random seeds.

    Problem:
    If the random seed is not set, the result will be irreproducible,
    which increases the debugging effort. In addition, it will be
    difficult to replicate the study based on the previous one. For example,
    in Scikit-Learn, if the random seed is not set, the random forest
    algorithm may provide a different result every time it runs, and the
    dataset split by cross-validation splitter will also be different in the
    next run.

    Solution:
    It is recommended to set global random seed first for
    reproducible results in Scikit-Learn, Pytorch, Numpy and other
    libraries where a random seed is involved. Specifically, DataLoader
    in PyTorch needs to be set with a random seed to ensure
    the data is split and loaded in the same way every time running the
    code.

    References:
    - https://pytorch.org/docs/stable/notes/randomness.html#reproducibility
    - https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
    """

    def __init__(self, filename):
        super().__init__(filename)

        # Nodes for code smell report
        self.torch_node = None
        self.py_node = None
        self.numpy_node = None
        self.sklearn_random_forest_node = None
        self.torch_dataloader_node = None

        # Call of random procedure indicators
        self.has_call_of_numpy_random = False  # Call of numpy.random())
        self.has_call_of_torch_rand = False  # Call of torch.rand()
        self.has_call_of_py_random = False  # Call of python random.random()

        # Seed and manual seed indicators
        self.has_numpy_seed = False  # Call of numpy.random.seed()
        self.has_py_seed = False  # Call of random.seed()
        self.has_torch_seed = False  # Call of torch.manual_seed()

        # PyTorch
        self.torch_dataloader_alias = set()
        self.has_torch_dataloader_param_worker_init_fn = False

        # Sklearn
        self.sklearn_random_forest_alias = set()
        self.has_sklearn_random_forest_parameter_random_state = False

        # Numpy
        self.numpy_alias = set()

        # Random
        self.py_random_alias = set()

    def visit_nodes(self, node: astroid.NodeNG) -> None:
        if isinstance(node, astroid.Import):
            self.check_import(node=node)
        elif isinstance(node, astroid.ImportFrom):
            self.check_importfrom_for_random_procedure_indicators(node=node)
            self.check_importfrom_for_explicit_set_of_random_seed(node=node)
            self.check_importfrom_for_function_code_smell(node=node)  # DataLoader and RandomForestClassifier
        elif isinstance(node, astroid.Call):
            self.check_call_for_random_procedure_indicators(node=node)
            self.check_call_for_explicit_set_of_random_seed(node=node)
            self.check_call_for_function_code_smell(node=node)

        for child in node.get_children():
            self.visit_nodes(child)

    def visit_module(self, module_node: astroid.Module) -> None:
        # Iterate module and search for indicators
        for node in module_node.body:
            self.visit_nodes(node)

        # Check for code smell
        self.check_randomness_uncontrolled()

    def check_import(self, node: astroid.Import) -> None:
        for name, alias in node.names:
            if name == "numpy":
                if node.names[0][1] is not None:
                    self.numpy_alias.add(node.names[0][1])
                else:
                    self.numpy_alias.add(node.names[0][0])
            if name == "random":
                if node.names[0][1] is not None:
                    self.py_random_alias.add(node.names[0][1])
                else:
                    self.py_random_alias.add(node.names[0][0])

    def check_importfrom_for_function_code_smell(self, node: astroid.ImportFrom):
        if "torch.utils.data" in node.modname:
            if "DataLoader" in node.names[0]:
                if node.names[0][1] is not None:
                    self.torch_dataloader_alias.add(node.names[0][1])
                else:
                    self.torch_dataloader_alias.add(node.names[0][0])
        elif "sklearn.ensemble" in node.modname:
            if "RandomForestClassifier" in node.names[0]:
                if node.names[0][1] is not None:
                    self.sklearn_random_forest_alias.add(node.names[0][1])
                else:
                    self.sklearn_random_forest_alias.add(node.names[0][0])

    def check_importfrom_for_random_procedure_indicators(self, node: astroid.ImportFrom):
        if node.modname == 'numpy' and any(name == 'random' for name, _ in node.names):
            self.has_call_of_numpy_random = True
        if node.modname == 'torch' and any(name == 'rand' for name, _ in node.names):
            self.has_call_of_torch_rand = True
        if node.modname == 'random':
            self.has_call_of_py_random = True

    def check_call_for_random_procedure_indicators(self, node: astroid.Call):
        # Check for random procedure indicators based on direct import of numpy/torch/random
        if isinstance(node.func, astroid.Attribute):
            if isinstance(node.func.expr, astroid.Attribute):
                try:
                    for infer in node.func.expr.inferred():
                        if isinstance(infer, astroid.Module):
                            if infer.name == "numpy.random":
                                self.has_call_of_numpy_random = True
                                self.numpy_node = node
                except astroid.InferenceError:
                    pass

            if isinstance(node.func.expr, astroid.Name):
                for infer in node.func.expr.inferred():
                    if isinstance(infer, astroid.Module):
                        # if infer.name == "numpy.random":
                        #     self.has_call_of_numpy_random = True
                        #     self.numpy_node = node
                        if infer.name == "random":
                            self.has_call_of_py_random = True
                            self.py_node = node
                        elif infer.name == "torch" and node.func.attrname == 'rand':
                            self.has_call_of_torch_rand = True
                            self.torch_node = node

    def check_importfrom_for_explicit_set_of_random_seed(self, node):
        if self.has_numpy_seed and self.has_torch_seed and self.has_py_seed:
            return

        if node.modname == 'numpy.random' and any(name == 'seed' for name, _ in node.names):
            self.has_numpy_seed = True
        if node.modname == 'torch' and any(name == 'manual_seed' for name, _ in node.names):
            self.has_torch_seed = True
        if node.modname == 'random' and any(name == 'seed' for name, _ in node.names):
            self.has_py_seed = True

    def check_call_for_explicit_set_of_random_seed(self, node: astroid.Call):
        if isinstance(node.func, astroid.Attribute):
            if node.func.attrname in {"seed", "manual_seed"}:

                if isinstance(node.func.expr, astroid.Attribute):
                    for infer in node.func.expr.inferred():
                        if isinstance(infer, astroid.Module):
                            if infer.name == "numpy.random":
                                self.has_numpy_seed = True

                if isinstance(node.func.expr, astroid.Name):
                    for infer in node.func.expr.inferred():
                        if isinstance(infer, astroid.Module):
                            if infer.name == "random":
                                self.has_py_seed = True
                            elif infer.name == "torch":
                                self.has_torch_seed = True

    def check_call_for_function_code_smell(self, node):
        self.check_torch_dataloader(node=node)
        self.check_sklearn_random_forest(node=node)

    def check_torch_dataloader(self, node: astroid.Call):
        if isinstance(node.func, astroid.Name) and node.func.name in self.torch_dataloader_alias:
            self.torch_dataloader_node = node
            for key in node.keywords:
                if key.arg == "worker_init_fn":
                    self.has_torch_dataloader_param_worker_init_fn = True

    def check_sklearn_random_forest(self, node):
        if isinstance(node.func, astroid.Name) and node.func.name in self.sklearn_random_forest_alias:
            self.sklearn_random_forest_node = node
            for key in node.keywords:
                if key.arg == "random_state":
                    self.has_sklearn_random_forest_parameter_random_state = True

    def check_randomness_uncontrolled(self):
        """
        1. Code smell - Use of SciKit RandomForestClassifier without setting random_state param and global Numpy seed
        2. Code smell - Use of PyTorch's DataLoader without setting NumPy's manual seed and setting worker_init_fn param
        3. Code smell - Use of NumPy's random without setting seed
        4. Code smell - Use of PyTorch's rand without setting seed
        5. Code smell - Use of Python's random without setting seed
        """
        # 1)
        if (
                self.sklearn_random_forest_alias
                and not self.has_sklearn_random_forest_parameter_random_state
                and not self.has_numpy_seed
                and self.sklearn_random_forest_node is not None
        ):
            self.record_finding(node=self.sklearn_random_forest_node)

        # 2)
        if (
                self.torch_dataloader_alias
                and not self.has_torch_seed
                and not self.has_torch_dataloader_param_worker_init_fn
                and self.torch_dataloader_node is not None
        ):
            self.record_finding(node=self.torch_dataloader_node)

        # 3)
        if (
                self.numpy_alias
                and not self.has_numpy_seed
                and self.has_call_of_numpy_random
                and self.numpy_node is not None
        ):
            self.record_finding(node=self.numpy_node)

        # 4)
        if (
                not self.has_torch_seed
                and self.has_call_of_torch_rand
                and self.torch_node is not None
        ):
            self.record_finding(node=self.torch_node)

        # 5)
        if (
                self.py_random_alias
                and not self.has_py_seed
                and self.has_call_of_py_random
                and self.py_node is not None
        ):
            self.record_finding(node=self.py_node)

    def record_finding(self, node: astroid.Call) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Randomness Uncontrolled",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="Set random seed explicitly during the development process whenever a "
                                         "possible random procedure is involved in the application.",
                             pipeline_stage="Model Training & Model Evaluation",
                             effect="Reproducibility",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
