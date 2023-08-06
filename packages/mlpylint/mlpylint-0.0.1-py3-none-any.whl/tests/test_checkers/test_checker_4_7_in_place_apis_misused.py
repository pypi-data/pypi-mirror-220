import os

from src.analysis.result import Result
from src.analysis.runner import Runner
from src.checkers.checker_4_7_in_place_apis_misused import InPlaceAPIsMisused

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERED_CHECKERS = [InPlaceAPIsMisused]


def test_checker_4_7_in_place_apis_misused():
    print(" Testing... \n")

    file_path = 'file_checker_4_7_in_place_apis_misused.py'
    absolute_file_path = os.path.join(ROOT_DIR, 'test_files', file_path)

    runner = Runner(path=absolute_file_path, registered_checkers=REGISTERED_CHECKERS)
    runner.run()

    assert len(Result.code_smells) == 2
