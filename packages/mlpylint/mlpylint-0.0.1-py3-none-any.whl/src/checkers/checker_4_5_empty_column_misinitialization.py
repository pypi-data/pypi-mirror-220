import astroid

from src.analysis.result import Result, CodeSmell
from src.checkers.base_checker import BaseChecker


class EmptyColumnMisinitialization(BaseChecker):
    """
    This class performs multiple checks involving the use of the "pandas" library and its "DataFrame" object: - It
    verifies the import of "pandas", storing its alias for future reference. - It checks for the direct import of
    "DataFrame" from 'pandas', and stores its alias as well. - It scrutinizes function calls for DataFrame object
    creation. When these are found, it extracts column names if explicitly provided, storing variable names and
    corresponding column names in a dictionary. - In the case of assignment operations, it reviews if the DataFrame
    columns are being assigned with zero or empty strings in several ways: - It checks for zero or empty string
    values being assigned to new columns via the 'assign' method. - It verifies direct column assignment (df['col'] =
    value) for zero or empty string values. - It checks multiple assignments to DataFrame columns where values are
    either zero or empty string. - If any of these checks pass, it records the code smell instance.

    Requirements to note: - When creating a DataFrame, the 'columns' keyword needs to be specified (e.g.,
    df = pd.DataFrame(data=data, columns=['A', 'B', 'C'])). - The usage of df.assign(A=value) and df["A"]=value should
    not be mixed, as values may become uninferable.
    """

    ID = "CS5"
    TITLE = "When a new empty column is needed in a DataFrame in Pandas, use the NaN value in Numpy instead of using " \
            "zeros or empty strings. "
    DESCRIPTION = """
    Context:
    Developers may need a new empty column in DataFrame.

    Problem:
    If they use zeros or empty strings to initialize a new
    empty column in Pandas, the ability to use methods such as .isnull()
    or .notnull() is retained. This might also happen to initializations
    in other data structure or libraries.

    Solution:
    Use NaN value (e.g. “np.nan”) if a new empty column in
    a DataFrame is needed. Do not use “filler values” such as zeros or
    empty strings.
    """

    def __init__(self, filename):
        super().__init__(filename)
        self.pandas_alias = set()
        self.pandas_dataframe_alias = set()
        self.dataframes = dict()

    def visit_import(self, node: astroid.Import) -> None:
        for name, alias in node.names:
            if name == "pandas":
                if alias is not None:
                    self.pandas_alias.add(alias)
                else:
                    self.pandas_alias.add(name)

    def visit_importfrom(self, node: astroid.ImportFrom) -> None:
        if node.modname == "pandas":
            for name, alias in node.names:
                if name in {"DataFrame"}:
                    if alias is not None:
                        self.pandas_dataframe_alias.add(alias)
                    else:
                        self.pandas_dataframe_alias.add(name)

    """
    Visits a 'Call' node. The function identifies the creation of DataFrame objects in the code.
    It checks if a DataFrame is being created and if so, extracts the column names if explicitly provided.
    The function handles both single and multiple assignment of DataFrame objects.
    It then updates 'self.dataframes' dictionary where the keys are variable names of the DataFrame
    objects and the values are sets of their column names.
    """
    def visit_call(self, node: astroid.Call) -> None:
        if isinstance(node.parent, astroid.Assign):
            func_name = None

            if (
                    isinstance(node.func, astroid.Attribute)
                    and isinstance(node.func.expr, astroid.Name)
                    and node.func.attrname == "DataFrame"
                    and (
                        node.func.expr.name in self.pandas_alias or
                        any(isinstance(i, astroid.Module) and i.name == 'pandas' for i in node.func.expr.inferred())
                    )
            ):
                # Pandas DataFrame is called by pandas alias, pd.DataFrame()
                func_name = node.func.attrname
            elif (
                    isinstance(node.func, astroid.Name)
                    and (
                            node.func.name in self.pandas_dataframe_alias or
                            any(isinstance(i, astroid.ClassDef) and i.name == 'DataFrame' for i in node.func.inferred())
                    )
            ):
                # Pandas DataFrame is called directly via importFrom and stored in pandas_dataframe_alias, DataFrame()
                func_name = node.func.name

            if func_name and func_name in self.pandas_dataframe_alias:
                # Extract column names
                col_names = [keyword.value for keyword in node.keywords if keyword.arg == 'columns']

                # if columns are explicitly set, and it is a list of column names
                if col_names and isinstance(col_names[0], astroid.List):
                    cols = self.extract_column_names(col_names[0])
                else:
                    cols = set()

                # Handle both single and multiple assignment
                targets = node.parent.targets[0]
                if isinstance(targets, astroid.AssignName):
                    # Single assignment
                    var_name = targets.name
                    self.dataframes[var_name] = cols
                elif isinstance(targets, astroid.Tuple):
                    # Multiple assignment
                    for target in targets.elts:
                        if isinstance(target, astroid.AssignName):
                            var_name = target.name
                            self.dataframes[var_name] = cols

    @staticmethod
    def extract_column_names(node: astroid.List) -> set:
        column_names = set()
        for elt in node.elts:
            if isinstance(elt, astroid.Const):
                column_names.add(elt.value)
        return column_names

    def visit_assign(self, node: astroid.Assign) -> None:
        # Check assign to DataFrame using .assign() method
        assign_target = node.targets[0] if node.targets else None
        if (
                assign_target is not None
                and isinstance(assign_target, astroid.AssignName)
                and assign_target.name in self.dataframes
                and isinstance(node.value, astroid.Call)
                and isinstance(node.value.func, astroid.Attribute)
                and node.value.func.attrname == 'assign'
        ):
            for keyword in node.value.keywords:
                if (
                        isinstance(keyword, astroid.Keyword)
                        and keyword.arg not in self.dataframes[assign_target.name]
                        and isinstance(keyword.value, astroid.Const)
                        and (keyword.value.value == 0 or keyword.value.value == "")
                ):
                    self.record_finding(node=node)
        if assign_target is not None:
            # Check assign to single subscript | df['Col'] = (0 or "")
            if (
                    # Check if assigned target is a stored DataFrame and if the column is new
                    isinstance(assign_target, astroid.Subscript)
                    and isinstance(assign_target.value, astroid.Name)
                    and assign_target.value.name in self.dataframes
                    and self.dataframes[assign_target.value.name]
                    and assign_target.ctx == astroid.Store
                    and isinstance(assign_target.slice, astroid.Const)
                    and assign_target.slice.value not in self.dataframes[assign_target.value.name]
            ):
                # Check if the value that is being assigned is "" or 0
                try:
                    if isinstance(node.value, astroid.Assign):
                        inferred_value = next(node.value.value.infer())
                    else:
                        inferred_value = next(node.value.infer())
                except astroid.InferenceError:
                    pass
                else:
                    if isinstance(inferred_value, astroid.Const) and inferred_value.value in {"", 0}:
                        self.record_finding(node=node)

            # Check assign to multiple subscripts
            # df['A'], df['G'], df['C'] = 0, "", ""
            # df['X'] = df['A'] = df['C'] = ""
            if isinstance(assign_target, astroid.Tuple):
                if isinstance(node.value, astroid.Tuple):
                    values = node.value.elts
                elif isinstance(node.value, astroid.Call):
                    # Handle the case when a function call is involved
                    values = [node.value] * len(assign_target.elts)
                else:
                    # Assume all targets get the same value
                    values = [node.value] * len(assign_target.elts)

                for target, value in zip(assign_target.elts, values):
                    if (
                            isinstance(target, astroid.Subscript)
                            and isinstance(target.value, astroid.Name)
                            and self.dataframes.get(target.value.name)  # Use get to avoid KeyError
                            and target.ctx == astroid.Store
                            and isinstance(target.slice, astroid.Const)
                            and target.slice.value not in self.dataframes[target.value.name]
                    ):
                        # Check if the value that is being assigned is "" or 0
                        try:
                            inferred_value = next(value.infer())
                        except astroid.InferenceError:
                            pass
                        else:
                            if isinstance(inferred_value, astroid.Const) and inferred_value.value in {"", 0}:
                                self.record_finding(node=node)

    def record_finding(self, node: astroid.Assign) -> None:
        Result.add(CodeSmell(code_smell_id=self.ID,
                             code_smell_title="Empty Column Misinitialization",
                             file_path=self.filename,
                             line=node.lineno,
                             col_offset=node.col_offset,
                             smell_type="Generic",
                             description="When a new empty column is needed in a DataFrame in Pandas, use the NaN "
                                         "value in Numpy instead of using zeros or empty strings.",
                             pipeline_stage="Data Cleaning",
                             effect="Robustness",
                             source_code=node.as_string(),
                             source_astroid_node=f"Astroid AST: {node} \n Code: {node.as_string()}"))
