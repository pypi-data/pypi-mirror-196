import numpy

from discrete_fuzzy_operators.base.operators.binary_operators.discrete.suboperators.fuzzy_discrete_implication_operator import DiscreteImplicationOperator
from discrete_fuzzy_operators.base.operators.binary_operators.discrete.suboperators.fuzzy_discrete_aggregation_suboperators.conjunction import Conjunction

from discrete_morphology.base.structuring_element import StructuringElement
from discrete_morphology.operators.erosion_dilation.discrete_dilation import discrete_dilation
from discrete_morphology.operators.erosion_dilation.discrete_erosion import discrete_erosion


def discrete_gradient(image: numpy.ndarray,
                      structuring_element: StructuringElement,
                      iterations_erosion: int,
                      iterations_dilation: int,
                      erosion_implication: DiscreteImplicationOperator,
                      dilation_conjunction: Conjunction):
    """
    Computes the discrete gradient of a grayscale image.

    Args:
        image: A numpy array, representing the image to be opened.
        structuring_element: A StructuringElement object, representing the properties and the shape of the
                             structuring element to be used.
        iterations_erosion: An integer, representing the number of iterations of the erosion.
        iterations_dilation: An integer, representing the number of iterations of the dilation.
        erosion_implication: A DiscreteImplicationOperator object, representing the implication to be used in the
                             erosion.
        dilation_conjunction: A Conjunction object, representing the conjunction to be used in the dilation.

    References:
        González-Hidalgo, M., & Massanet, S. (2014).
        A fuzzy mathematical morphology based on discrete t-norms: fundamentals and applications to image processing.
        Soft Computing, 18 (11), 2297–2311. https://doi.org/10.1007/s00500-013-1204-6

    Returns:
        An image with the same dimension as the input image, representing the gradient of the image.
    """
    dilation = discrete_dilation(image=image,
                                 structuring_element=structuring_element,
                                 iterations=iterations_dilation,
                                 conjunction=dilation_conjunction)
    erosion = discrete_erosion(image=image,
                               structuring_element=structuring_element,
                               iterations=iterations_erosion,
                               implication=erosion_implication)
    return dilation-erosion
