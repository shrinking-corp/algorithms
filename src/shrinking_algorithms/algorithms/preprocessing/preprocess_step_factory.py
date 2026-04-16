from shrinking_algorithms.algorithms.preprocessing.attribute_strategies import RandomAttributeRemovalStrategy, RemoveAttributesByVisibilityStrategy
from shrinking_algorithms.algorithms.preprocessing.preprocess_base import PreprocessStep
from shrinking_algorithms.algorithms.preprocessing.preprocess_step import (
    RemoveAttributesStep,
    RemoveClassesStep,
    RemoveMethodsStep,
    RemoveEdgesStep,
)
    
from shrinking_algorithms.algorithms.preprocessing.class_strategies import (
    RandomClassRemovalStrategy,
    RemoveEmptyClassesStrategy,
    RemoveIsolatedClassesStrategy,
    RemoveLeafClassesStrategy,
    RemoveLowDegreeClassesStrategy,
)

from shrinking_algorithms.algorithms.preprocessing.method_strategies import (
    RandomMethodRemovalStrategy,
    RemoveMethodsByVisibilityStrategy,
    RemoveGettersAndSettersStrategy,
)

from shrinking_algorithms.algorithms.preprocessing.edge_strategies import (
    RandomEdgeRemovalStrategy,
)

from shrinking_algorithms.algorithms.preprocessing.types import Visibility


class PreprocessStepFactory:

    def get_step(self, step_id: str)-> PreprocessStep:
        if step_id == "remove_random_classes":
            return RemoveClassesStep(RandomClassRemovalStrategy(0.5))
        elif step_id == "remove_empty_classes":
            return RemoveClassesStep(RemoveEmptyClassesStrategy())
        elif step_id == "remove_isolated_classes":
            return RemoveClassesStep(RemoveIsolatedClassesStrategy())
        elif step_id == "remove_leaf_classes":
            return RemoveClassesStep(RemoveLeafClassesStrategy())
        elif step_id == "remove_low_degree_classes":
            return RemoveClassesStep(RemoveLowDegreeClassesStrategy(2))
        elif step_id == "remove_random_methods":
            return RemoveMethodsStep(RandomMethodRemovalStrategy(0.5))
        elif step_id == "remove_getters_and_setters":
            return RemoveMethodsStep(RemoveGettersAndSettersStrategy())
        elif step_id == "remove_public_methods":
            return RemoveMethodsStep(RemoveMethodsByVisibilityStrategy(Visibility.PUBLIC))
        elif step_id == "remove_private_methods":
            return RemoveMethodsStep(RemoveMethodsByVisibilityStrategy(Visibility.PRIVATE))
        elif step_id == "remove_protected_methods":
            return RemoveMethodsStep(RemoveMethodsByVisibilityStrategy(Visibility.PROTECTED))
        elif step_id == "remove_package_methods":
            return RemoveMethodsStep(RemoveMethodsByVisibilityStrategy(Visibility.PACKAGE))
        elif step_id == "remove_random_edges":
            return RemoveEdgesStep(RandomEdgeRemovalStrategy(0.5))
        elif step_id == "remove_random_attributes":
            return RemoveAttributesStep(RandomAttributeRemovalStrategy(0.5))
        elif step_id == "remove_public_attributes": 
            return RemoveAttributesStep(RemoveAttributesByVisibilityStrategy(Visibility.PUBLIC))
        elif step_id == "remove_private_attributes":
            return RemoveAttributesStep(RemoveAttributesByVisibilityStrategy(Visibility.PRIVATE))
        elif step_id == "remove_protected_attributes":
            return RemoveAttributesStep(RemoveAttributesByVisibilityStrategy(Visibility.PROTECTED))
        elif step_id == "remove_package_attributes":
            return RemoveAttributesStep(RemoveAttributesByVisibilityStrategy(Visibility.PACKAGE))
        else:
            raise ValueError(f"Unknown step id: {step_id}")
    
