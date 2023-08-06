import os

from src.analysis.result import Result
from src.analysis.runner import Runner
from src.checkers.advice.advice_checker_4_16_broadcasting_feature_not_used import BroadcastingFeatureNotUsed

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERED_CHECKERS = [BroadcastingFeatureNotUsed]


def test_advice_checker_4_16_broadcasting_feature_not_used():
    print(" Testing... \n")

    file_path = 'file_checker_4_16_broadcasting_feature_not_used.py'
    absolute_file_path = os.path.join(ROOT_DIR, 'test_files', file_path)

    runner = Runner(path=absolute_file_path, registered_checkers=REGISTERED_CHECKERS)
    runner.run()

    assert len(Result.code_smells) == 1  # Advice should stop after single detection of code smell
