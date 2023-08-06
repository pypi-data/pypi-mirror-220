from typing import Any, Dict, List, TypedDict, Union

WithArgs = Dict[str, Any]

TransformSchema = TypedDict(
    "TransformSchema",
    {
        "transform": str,
        "with": WithArgs,
    },
    total=False,
)


class _CursorSchema(TypedDict, total=False):
    version: int


class CursorSchema(_CursorSchema):
    on: str
    perform: Union[List[TransformSchema], TransformSchema]
