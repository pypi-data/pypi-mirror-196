import numpy
from typing import Tuple

from discrete_morphology.base.exceptions.structuring_element_out_bounds import StructuringElementOutOfBounds


class StructuringElement:
    """
    Object that represents the structuring element, with its matrix and its center.
    """

    def __init__(self, structuring_element_matrix: numpy.ndarray, center: Tuple[int, int]):
        """
        Initializes the object that represents the structuring element.

        Args:
            structuring_element_matrix: A numpy array, representing the matrix representation of the structuring element.
            center: A tuple of two integers, representing the coordinates of the center of the structuring element.
        """
        self.structuring_element_matrix = structuring_element_matrix
        self.center = center

    @property
    def dimension(self):
        """
        Returns the dimensions of the structuring element.
        """
        return self.structuring_element_matrix.shape

    def get_reflected_structuring_element(self) -> "StructuringElement":
        """
        Generates the reflected structuring element; that is, if B(x,y) represents the matrix of the structuring element,
        its reflection is defined as B(m-x,n-y), where m and n are the maximum values of the domain.

        Returns:
            A StructuringElement object, representing the reflection of the object.
        """
        reflected_matrix = numpy.fliplr(numpy.flipud(self.structuring_element_matrix))
        return StructuringElement(structuring_element_matrix=reflected_matrix,
                                  center=self.center)

    def evaluate(self, x: int, y: int) -> int:
        """
        Evaluates the structuring element in a point.

        Args:
            x: An integer, representing the first coordinate of the point to evaluate.
            y: An integer, representing the second coordinate of the point to evaluate.

        Returns:
            An integer, representing the value B(x, y).
        """
        rows, columns = self.structuring_element_matrix.shape

        if (0 <= x < columns) and (0 <= y < rows):
            return self.structuring_element_matrix[x, y]
        else:
            raise StructuringElementOutOfBounds
