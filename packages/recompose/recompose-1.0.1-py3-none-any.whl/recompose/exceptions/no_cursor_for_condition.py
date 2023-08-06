from recompose.exceptions.recompose import RecomposeError


class NoCursorForCondition(RecomposeError):
    """
    Raised when there are no cursors to satisfy a given condition.
    """

    def __init__(self, condition: str) -> None:
        super().__init__('No cursors can satisfy condition "%s"' % condition)
