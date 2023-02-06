"""Types for geojson_pydantic models"""

from typing import Generator, List, Tuple, Union

from pydantic import ConstrainedList, PydanticValueError

BBox = Union[
    Tuple[float, float, float, float],  # 2D bbox
    Tuple[float, float, float, float, float, float],  # 3D bbox
]
Position = Union[Tuple[float, float], Tuple[float, float, float]]

MultiPointCoords = List[Position]


class NotClosedError(PydanticValueError):
    """Custom PydanticValueError for LinearRing that is not closed."""

    code = "linearring.not_closed"
    msg_template = (
        "first position {first} and last position {last} must contain identical values"
    )

    def __init__(self, *, first: Position, last: Position) -> None:
        """Overload init to take in the positions."""
        super().__init__(first=first, last=last)


class LinearRing(ConstrainedList):
    """Custom ConstrainedList to perform validation of LinearRing within the type."""

    min_items = 4
    item_type = Position  # type: ignore
    __args__ = (Position,)  # type: ignore

    @classmethod
    def __get_validators__(cls) -> Generator:
        """Yield the base validators then the closed validator."""
        yield from super().__get_validators__()
        yield cls.closed_validator

    @classmethod
    def closed_validator(cls, v: List[Position]) -> List[Position]:
        """Validate that the LinearRing is closed."""
        if v[0] != v[-1]:
            raise NotClosedError(first=v[0], last=v[-1])
        return v


class LineStringCoords(ConstrainedList):
    """Custom ConstrainedList for LineString."""

    min_items = 2
    item_type = Position  # type: ignore
    __args__ = (Position,)  # type: ignore


MultiLineStringCoords = List[LineStringCoords]

PolygonCoords = List[LinearRing]
MultiPolygonCoords = List[PolygonCoords]
