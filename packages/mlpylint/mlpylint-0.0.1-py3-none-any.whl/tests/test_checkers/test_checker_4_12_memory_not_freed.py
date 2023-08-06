import os

from src.analysis.result import Result
from src.analysis.runner import Runner
from src.checkers.advice.advice_checker_4_12_memory_not_freed import MemoryNotFreed

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERED_CHECKERS = [MemoryNotFreed]


def test_advice_checker_4_12_memory_not_freed():
    print(" Testing... \n")

    file_path = 'file_checker_4_12_memory_not_freed.py'
    absolute_file_path = os.path.join(ROOT_DIR, 'test_files', file_path)

    runner = Runner(path=absolute_file_path, registered_checkers=REGISTERED_CHECKERS)
    runner.run()

    assert len(Result.code_smells) == 2
