
class BaseChecker:
    """
    BaseChecker class for recursively iterating all nodes within an ast-module

    - Future work within code-smells domain specific (timeseries, images, natural language/text processing)
    """

    def __init__(self, filename):
        self.filename = filename

    def visit(self, node):
        method_name = f"visit_{node.__class__.__name__.lower()}"
        if hasattr(self, method_name):
            getattr(self, method_name)(node)
        for child in node.get_children():
            self.visit(child)
