class StructuringElementOutOfBounds(Exception):
    """
    An Exception which indicates that the coordinates of the point where the structuring element is evaluated is
    out of its domain.
    """

    def __init__(self, message: str = "The coordinates of the point where the structuring element is evaluated is"
                                      "out of its domain."):
        super().__init__(message)