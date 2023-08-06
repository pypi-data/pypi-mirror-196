import numpy

from discrete_fuzzy_operators.base.operators.binary_operators.discrete.suboperators.fuzzy_discrete_aggregation_suboperators.conjunction import Conjunction

from discrete_morphology.base.structuring_element import StructuringElement


def discrete_dilation(image: numpy.ndarray,
                      structuring_element: StructuringElement,
                      iterations: int,
                      conjunction: Conjunction) -> numpy.ndarray:
    """
    Applies the discrete dilation to a grayscale image.

    Args:
        image: A numpy array, representing the image to be dilated.
        structuring_element: A StructuringElement object, representing the properties and the shape of the
                             structuring element to be used.
        iterations: An integer, representing the number of times that the dilation has to be applied to the image.
        conjunction: A Conjunction object, representing the conjunction to be used.

    References:
        González-Hidalgo, M., & Massanet, S. (2014).
        A fuzzy mathematical morphology based on discrete t-norms: fundamentals and applications to image processing.
        Soft Computing, 18 (11), 2297–2311. https://doi.org/10.1007/s00500-013-1204-6

    Returns:
        An image with the same dimension as the input image, representing the dilated image.
    """

    img_rows, img_columns = image.shape
    se_rows, se_columns = structuring_element.dimension

    dilation_result = image.copy()

    iteration = image.copy()
    for _ in range(0, iterations):

        for i in range(0, img_rows):
            for j in range(0, img_columns):
                max_value = 0

                for ii in range(0, se_rows):
                    for jj in range(0, se_columns):
                        try:
                            x_value = structuring_element.evaluate(x=jj, y=ii)
                            y_value = iteration[
                                i + ii - structuring_element.center[0], j + jj - structuring_element.center[1]]

                            t_norm_value = conjunction.evaluate_operator(x=x_value, y=y_value)

                            if t_norm_value > max_value:
                                max_value = t_norm_value
                        except:
                            continue
                dilation_result[i, j] = max_value
        iteration = dilation_result.copy()

    return dilation_result
