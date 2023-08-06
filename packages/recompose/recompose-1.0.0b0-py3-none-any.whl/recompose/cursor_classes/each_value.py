from typing import Any, Dict, List, Union

from recompose.cursor import Cursor
from recompose.logging import log

ListOrDict = Union[List[Any], Dict[Any, Any]]


class EachValue(Cursor):
    """
    A cursor that expects and yields each value in a list or dictionary.
    """

    def _transform(
        self,
        data: ListOrDict,
    ) -> ListOrDict:
        result: ListOrDict = {} if isinstance(data, dict) else []

        for sub in data:
            # "sub" will be a value if "data" is a list or a key if "data" is a
            # dictionary.
            #
            # Either way, "child" will be the value to transform.
            child = data[sub] if isinstance(data, dict) else sub

            log.debug("%s transforming child item %s", self, child)

            for transformer in self.transformers:
                transformed = transformer.transform(child)

                log.debug(
                    "%s transformed child item %s to %s",
                    self,
                    child,
                    transformed,
                )

                if isinstance(result, dict):
                    result[sub] = transformed
                else:
                    result.append(transformed)

        return result

    @classmethod
    def condition(cls) -> str:
        return "each-value"
