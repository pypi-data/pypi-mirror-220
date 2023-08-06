from recompose.exceptions.recompose import RecomposeError


class NotATransformerType(RecomposeError):
    """
    Raised when a query does not match any transformer types.
    """

    def __init__(self, name: str) -> None:
        super().__init__('No registered transformers named "%s"' % name)
