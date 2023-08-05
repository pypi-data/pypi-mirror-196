from dataclasses import dataclass
from typing import Any, TypeVar

from typing_extensions import Annotated, TypeAlias

from combadge.core.markers.parameter import ParameterMarker
from combadge.support.rest.abc import SupportsJson

_T = TypeVar("_T")


@dataclass
class JsonParameterMarker(ParameterMarker[SupportsJson]):
    """
    Marker class for the [`Json`][combadge.support.rest.markers.Json] alias.

    Used for a more complex annotations, for example:

    ```python
    Annotated[BodyModel, JsonParameterMarker(), AnotherMarker]
    ```
    """

    __slots__ = ()

    def prepare_request(self, request: SupportsJson, value: Any) -> None:  # noqa: D102
        request.json_ = value


Json: TypeAlias = Annotated[_T, JsonParameterMarker()]
"""
Mark parameter as a request JSON body. An argument gets converted to a dictionary and passed over to a backend.

Examples:
    >>> from combadge.support.rest.markers import Json
    >>>
    >>> class BodyModel(BaseModel):
    >>>     ...
    >>>
    >>> def call(body: Json[BodyModel]) -> ...:
    >>>     ...
"""


@dataclass
class JsonFieldParameterMarker(ParameterMarker[SupportsJson]):
    """
    Marker class for the [`JsonField`][combadge.support.rest.markers.JsonField] alias.

    It's recommended that you use the alias, unless you need a complex annotation, such as:
    ```python
    parameter: Annotated[int, JsonFieldParameterMarker("param"), AnotherMarker()]
    ```
    """

    name: str
    __slots__ = ("name",)

    def prepare_request(self, request: SupportsJson, value: Any) -> None:  # noqa: D102
        request.json_fields[self.name] = value


JsonField: TypeAlias = JsonFieldParameterMarker
"""
Mark a parameter as a separate JSON field value.

Examples:
    >>> from combadge.support.rest.markers import JsonField
    >>>
    >>> def call(param: Annotated[int, JsonField("param")]) -> ...:
    >>>     ...

Notes:
    - [`Json`][combadge.support.rest.markers.Json] marker's fields shadow `JsonField` ones (if present)
"""
