import textwrap
from typing import List, Type

from src.checkers.advice.advice_checker_4_12_memory_not_freed import MemoryNotFreed
from src.checkers.advice.advice_checker_4_16_broadcasting_feature_not_used import BroadcastingFeatureNotUsed
from src.checkers.advice.advice_checker_4_18_training_evaluation_mode_improper_toggling import \
    TrainingAndEvaluationModeImproperToggling
from src.checkers.advice.advice_checker_4_1_unnecessary_iteration import UnnecessaryIteration
from src.checkers.advice.advice_checker_4_20_gradients_not_cleared_before_backward_propagation import \
    GradientsNotClearedBeforeBackwardPropagation
from src.checkers.base_checker import BaseChecker
from src.checkers.checker_4_11_hyperparameter_not_explicitly_set import HyperparameterNotExplicitlySet
from src.checkers.checker_4_13_deterministic_algorithm_option_not_used import DeterministicAlgorithmOptionNotUsed
from src.checkers.checker_4_14_randomness_uncontrolled import RandomnessUncontrolled
from src.checkers.checker_4_15_missing_the_mask_of_invalid_value import MissingTheMaskOfInvalidValue
from src.checkers.checker_4_17_tensorarray_not_used import TensorArrayNotUsed
from src.checkers.checker_4_19_pytorch_call_method_misused import PytorchCallMethodMisused
from src.checkers.advice.advice_checker_4_21_data_leakage import DataLeakage
from src.checkers.checker_4_2_nan_equivalence_comparison_misused import NaNEquivalenceComparisonMisusedChecker
from src.checkers.checker_4_3_chain_indexing import ChainIndexing
from src.checkers.checker_4_4_columns_and_data_type_not_explicitly_set import ColumnsAndDataTypeNotExplicitlySet
from src.checkers.checker_4_5_empty_column_misinitialization import EmptyColumnMisinitialization
from src.checkers.checker_4_6_merge_api_parameter_not_explicitly_set import MergeAPIParameterNotExplicitlySet
from src.checkers.checker_4_7_in_place_apis_misused import InPlaceAPIsMisused
from src.checkers.checker_4_8_dataframe_conversion_api_misused import DataframeConversionAPIMisused
from src.checkers.checker_4_9_matrix_multiplication_api_misused import MatrixMultiplicationAPIMisused

REGISTERED_CHECKERS: List[Type[BaseChecker]] = [
    NaNEquivalenceComparisonMisusedChecker,
    ChainIndexing,
    ColumnsAndDataTypeNotExplicitlySet,
    EmptyColumnMisinitialization,
    MergeAPIParameterNotExplicitlySet,
    InPlaceAPIsMisused,
    DataframeConversionAPIMisused,
    MatrixMultiplicationAPIMisused,
    HyperparameterNotExplicitlySet,
    DeterministicAlgorithmOptionNotUsed,
    RandomnessUncontrolled,
    MissingTheMaskOfInvalidValue,
    TensorArrayNotUsed,
    PytorchCallMethodMisused
]

REGISTERED_CHECKERS_ADVICE: List[Type[BaseChecker]] = [
    UnnecessaryIteration,
    MemoryNotFreed,
    BroadcastingFeatureNotUsed,
    TrainingAndEvaluationModeImproperToggling,
    GradientsNotClearedBeforeBackwardPropagation,
    DataLeakage
]


class ArgumentConfig:
    @staticmethod
    def handle_list_smells():
        """Prints all the IDs of the registered code smells"""

        code_smells = {
            UnnecessaryIteration.ID: UnnecessaryIteration.TITLE,
            NaNEquivalenceComparisonMisusedChecker.ID: NaNEquivalenceComparisonMisusedChecker.TITLE,
            ChainIndexing.ID: ChainIndexing.TITLE,
            ColumnsAndDataTypeNotExplicitlySet.ID: ColumnsAndDataTypeNotExplicitlySet.TITLE,
            EmptyColumnMisinitialization.ID: EmptyColumnMisinitialization.TITLE,
            MergeAPIParameterNotExplicitlySet.ID: MergeAPIParameterNotExplicitlySet.TITLE,
            InPlaceAPIsMisused.ID: InPlaceAPIsMisused.TITLE,
            DataframeConversionAPIMisused.ID: DataframeConversionAPIMisused.TITLE,
            MatrixMultiplicationAPIMisused.ID: MatrixMultiplicationAPIMisused.TITLE,
            HyperparameterNotExplicitlySet.ID: HyperparameterNotExplicitlySet.TITLE,
            MemoryNotFreed.ID: MemoryNotFreed.TITLE,
            DeterministicAlgorithmOptionNotUsed.ID: DeterministicAlgorithmOptionNotUsed.TITLE,
            RandomnessUncontrolled.ID: RandomnessUncontrolled.TITLE,
            MissingTheMaskOfInvalidValue.ID: MissingTheMaskOfInvalidValue.TITLE,
            BroadcastingFeatureNotUsed.ID: BroadcastingFeatureNotUsed.TITLE,
            TensorArrayNotUsed.ID: TensorArrayNotUsed.TITLE,
            TrainingAndEvaluationModeImproperToggling.ID: TrainingAndEvaluationModeImproperToggling.TITLE,
            PytorchCallMethodMisused.ID: PytorchCallMethodMisused.TITLE,
            GradientsNotClearedBeforeBackwardPropagation.ID: GradientsNotClearedBeforeBackwardPropagation.TITLE,
            DataLeakage.ID: DataLeakage.TITLE,
        }

        print('Id  | Code smell')
        for key, descr in code_smells.items():
            print(key, ":", descr)

    @staticmethod
    def handle_describe_smell(smell_id: str):
        """Prints the description of a specific code smell given its ID"""
        smell_id = smell_id.upper()
        code_smells = {
            UnnecessaryIteration.ID: UnnecessaryIteration.DESCRIPTION,
            NaNEquivalenceComparisonMisusedChecker.ID: NaNEquivalenceComparisonMisusedChecker.DESCRIPTION,
            ChainIndexing.ID: ChainIndexing.DESCRIPTION,
            ColumnsAndDataTypeNotExplicitlySet.ID: ColumnsAndDataTypeNotExplicitlySet.DESCRIPTION,
            EmptyColumnMisinitialization.ID: EmptyColumnMisinitialization.DESCRIPTION,
            MergeAPIParameterNotExplicitlySet.ID: MergeAPIParameterNotExplicitlySet.DESCRIPTION,
            InPlaceAPIsMisused.ID: InPlaceAPIsMisused.DESCRIPTION,
            DataframeConversionAPIMisused.ID: DataframeConversionAPIMisused.DESCRIPTION,
            MatrixMultiplicationAPIMisused.ID: MatrixMultiplicationAPIMisused.DESCRIPTION,
            HyperparameterNotExplicitlySet.ID: HyperparameterNotExplicitlySet.DESCRIPTION,
            MemoryNotFreed.ID: MemoryNotFreed.DESCRIPTION,
            DeterministicAlgorithmOptionNotUsed.ID: DeterministicAlgorithmOptionNotUsed.DESCRIPTION,
            RandomnessUncontrolled.ID: RandomnessUncontrolled.DESCRIPTION,
            MissingTheMaskOfInvalidValue.ID: MissingTheMaskOfInvalidValue.DESCRIPTION,
            BroadcastingFeatureNotUsed.ID: BroadcastingFeatureNotUsed.DESCRIPTION,
            TensorArrayNotUsed.ID: TensorArrayNotUsed.DESCRIPTION,
            TrainingAndEvaluationModeImproperToggling.ID: TrainingAndEvaluationModeImproperToggling.DESCRIPTION,
            PytorchCallMethodMisused.ID: PytorchCallMethodMisused.DESCRIPTION,
            GradientsNotClearedBeforeBackwardPropagation.ID: GradientsNotClearedBeforeBackwardPropagation.DESCRIPTION,
            DataLeakage.ID: DataLeakage.DESCRIPTION,
        }

        if smell_id in code_smells:
            print(f'{smell_id}: {textwrap.dedent(code_smells[smell_id])}')
        else:
            print(f'No code smell found with ID {smell_id}')
