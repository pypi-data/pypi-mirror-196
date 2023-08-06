from typing import Tuple

import numpy

from discrete_fuzzy_operators.base.operators.binary_operators.discrete.suboperators.fuzzy_discrete_implication_operator import DiscreteImplicationOperator
from discrete_morphology.base.structuring_element import StructuringElement


def discrete_erosion(image: numpy.ndarray,
                     structuring_element: StructuringElement,
                     iterations: int,
                     implication: DiscreteImplicationOperator) -> numpy.ndarray:
    """
    Applies the discrete erosion to a grayscale image.

    Args:
        image: A numpy array, representing the image to be eroded.
        structuring_element: A StructuringElement object, representing the properties and the shape of the
                             structuring element to be used.
        iterations: An integer, representing the number of times that the erosion has to be applied to the image.
        implication: A DiscreteImplicationOperator object, representing the implication to be used.

    References:
        González-Hidalgo, M., & Massanet, S. (2014).
        A fuzzy mathematical morphology based on discrete t-norms: fundamentals and applications to image processing.
        Soft Computing, 18 (11), 2297–2311. https://doi.org/10.1007/s00500-013-1204-6

    Returns:
        An image with the same dimension as the input image, representing the eroded image.
    """
    img_rows, img_columns = image.shape
    se_rows, se_columns = structuring_element.dimension

    erosion_result = image.copy()

    iteration = image.copy()
    for _ in range(0, iterations):

        for i in range(0, img_rows):
            for j in range(0, img_columns):
                min_value = 255

                for ii in range(0, se_rows):
                    for jj in range(0, se_columns):
                        try:
                            x_value = structuring_element.evaluate(x=jj, y=ii)
                            y_value = iteration[i+ii-structuring_element.center[0], j+jj-structuring_element.center[1]]

                            implication_value = implication.evaluate_operator(x=x_value, y=y_value)

                            if implication_value < min_value:
                                min_value = implication_value
                        except:
                            continue
                erosion_result[i, j] = min_value
        iteration = erosion_result.copy()

    return erosion_result
