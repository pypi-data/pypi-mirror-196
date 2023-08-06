import numpy

from discrete_fuzzy_operators.base.operators.binary_operators.suboperators.fuzzy_implication_operator import DiscreteFuzzyImplicationOperator
from discrete_fuzzy_operators.base.operators.binary_operators.suboperators.fuzzy_aggregation_operator import DiscreteFuzzyAggregationBinaryOperator
from discrete_morphology.base.structuring_element import StructuringElement
from discrete_morphology.operators.erosion_dilation.discrete_dilation import discrete_dilation
from discrete_morphology.operators.erosion_dilation.discrete_erosion import discrete_erosion


def discrete_opening(image: numpy.ndarray,
                     structuring_element: StructuringElement,
                     iterations: int,
                     erosion_implication: DiscreteFuzzyImplicationOperator,
                     dilation_tnorm: DiscreteFuzzyAggregationBinaryOperator):
    """
    Applies the discrete opening to a grayscale image.

    Args:
        image: A numpy array, representing the image to be opened.
        structuring_element: A StructuringElement object, representing the properties and the shape of the
                             structuring element to be used.
        iterations: An integer, representing the number of times that the opening has to be applied to the image.
        erosion_implication: A DiscreteFuzzyImplicationOperator object, representing the implication to be used in the
                             erosion.
        dilation_tnorm: A DiscreteFuzzyAggregationBinaryOperator object, representing the t-norm to be used in the
                        dilation.

    References:
        González-Hidalgo, M., & Massanet, S. (2014).
        A fuzzy mathematical morphology based on discrete t-norms: fundamentals and applications to image processing.
        Soft Computing, 18 (11), 2297–2311. https://doi.org/10.1007/s00500-013-1204-6

    Returns:
        An image with the same dimension as the input image, representing the opened image.
    """
    result = image.copy()
    for _ in range(0, iterations):
        erosion = discrete_erosion(image=result,
                                   structuring_element=structuring_element,
                                   iterations=1,
                                   implication=erosion_implication)
        dilation = discrete_dilation(image=erosion,
                                     structuring_element=structuring_element.get_reflected_structuring_element(),
                                     iterations=1,
                                     t_norm=dilation_tnorm)

        result = dilation
    return result
