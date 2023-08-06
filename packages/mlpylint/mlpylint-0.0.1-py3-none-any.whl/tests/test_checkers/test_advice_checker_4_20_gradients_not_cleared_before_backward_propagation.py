import os

from src.analysis.result import Result
from src.analysis.runner import Runner
from src.checkers.advice.advice_checker_4_20_gradients_not_cleared_before_backward_propagation import \
    GradientsNotClearedBeforeBackwardPropagation

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERED_CHECKERS = [GradientsNotClearedBeforeBackwardPropagation]


def test_advice_checker_4_20_gradients_not_cleared_before_backward_propagation():
    print(" Testing... \n")

    file_path = 'file_checker_4_20_gradients_not_cleared_before_backward_propagation.py'
    absolute_file_path = os.path.join(ROOT_DIR, 'test_files', file_path)

    runner = Runner(path=absolute_file_path, registered_checkers=REGISTERED_CHECKERS)
    runner.run()

    assert len(Result.code_smells) == 1  # Advice should stop after single detection of code smell
