import os

from src.analysis.result import Result
from src.analysis.runner import Runner
from src.checkers.checker_4_4_columns_and_data_type_not_explicitly_set import ColumnsAndDataTypeNotExplicitlySet

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERED_CHECKERS = [ColumnsAndDataTypeNotExplicitlySet]


def test_checker_4_4_columns_and_data_type_not_explicitly():
    print(" Testing... \n")

    file_path = 'file_checker_4_4_columns_and_datatype_not_explicitly_set.py'
    absolute_file_path = os.path.join(ROOT_DIR, 'test_files', file_path)

    runner = Runner(path=absolute_file_path, registered_checkers=REGISTERED_CHECKERS)
    runner.run()

    assert len(Result.code_smells) == 5
