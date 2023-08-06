from typing import Any, Dict, List, TypedDict, Union

TransformSchema = Dict[str, Any]

AnyTransformSchema = Union[Dict[str, Any], str]


class _CursorSchema(TypedDict, total=False):
    on: str
    """
    Condition. Defaults to "this-value" if omitted.
    """

    version: int


class CursorSchema(_CursorSchema):
    perform: Union[List[TransformSchema], TransformSchema]
