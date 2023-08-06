from enum import Enum
from typing import Any, Callable, Iterator, Literal, TypeAlias, cast

import daiquiri
import isodate
import pandas as pd
import webcolors
from isodate import Duration
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pydantic import BaseModel, Field, StrictStr, validator
from webcolors import IntegerRGB

from dbnomics_pptx_tools.module_utils import parse_callable

logger = daiquiri.getLogger(__name__)


class DataLabelPosition(Enum):
    LAST_POINT = "last_point"


ChartName: TypeAlias = str
DataLabelType: TypeAlias = Literal["last_point"]
Frequency: TypeAlias = Literal["annual", "monthly", "quarterly"]
SeriesId: TypeAlias = str
SeriesFactory: TypeAlias = Callable[..., pd.Series]
SeriesTransformer: TypeAlias = Callable[[pd.Series], pd.Series]
TableLocation: TypeAlias = str


def parse_entry_point(value: str) -> Callable[..., Any]:
    if not isinstance(value, str):
        raise ValueError(f"str expected, got {type(value)}")
    function = parse_callable(value)
    if function is None:
        raise ValueError(f"The function referenced by {value!r} does not exist")
    return function


class FactorySpec(BaseModel):
    function: SeriesFactory
    parameters: dict[str, str] = Field(default_factory=dict)

    _parse_entry_point = validator("function", allow_reuse=True, pre=True)(parse_entry_point)


class SeriesFormatSpec(BaseModel):
    color: IntegerRGB | None = None
    dash_style: int | None = None
    width: int | None = None

    class Config:
        arbitrary_types_allowed = True

    @validator("color", pre=True)
    def parse_color(cls, value: str) -> IntegerRGB:
        if not isinstance(value, str):
            raise ValueError(f"str expected, got {type(value)}")
        return webcolors.name_to_rgb(value)

    @validator("dash_style", pre=True)
    def parse_dash_style(cls, value: str) -> int:
        if not isinstance(value, str):
            raise ValueError(f"str expected, got {type(value)}")
        try:
            return cast(int, getattr(MSO_LINE_DASH_STYLE, value))
        except AttributeError as exc:
            available = [member.name for member in MSO_LINE_DASH_STYLE.__members__]
            raise ValueError(f"Invalid dash_style: {value!r}. Available values: {available!r}") from exc


class SeriesSpec(BaseModel):
    id: str
    name: str

    format: SeriesFormatSpec | None = None
    factory: FactorySpec | None = None
    transformers: list[SeriesTransformer] = Field(default_factory=list)

    _parse_entry_point = validator("transformers", allow_reuse=True, each_item=True, pre=True)(parse_entry_point)

    def is_fetchable(self) -> bool:
        return self.factory is None


class ShapeSpec(BaseModel):
    data_sources: list[SeriesId] = Field(default_factory=list)
    series: list[SeriesSpec]

    def find_fetchable_series_ids(self) -> list[SeriesId]:
        return [series_spec.id for series_spec in self.series if series_spec.is_fetchable()]

    @validator("series")
    def validate_series_name_is_unique(cls, value: list[SeriesSpec]) -> list[SeriesSpec]:
        series_names = {series_spec.name for series_spec in value}
        if len(series_names) != len(value):
            raise ValueError("Series names must be unique")
        return value


class DataLabelSpec(BaseModel):
    type: DataLabelType
    number_format: StrictStr = "0.0"


class ChartSpec(ShapeSpec):
    data_labels: list[DataLabelType | DataLabelSpec] = Field(default_factory=list)

    def iter_data_label_specs(self) -> Iterator[DataLabelSpec]:
        for data_label in self.data_labels:
            if isinstance(data_label, str):
                yield DataLabelSpec(type=data_label)
            else:
                yield data_label


class ColumnsSpec(BaseModel):
    end_period_offset: Duration | None
    frequency: Frequency
    period_format: str

    class Config:
        arbitrary_types_allowed = True

    @validator("end_period_offset", pre=True)
    def parse_end_period_offset(cls, value: str) -> Duration:
        if not isinstance(value, str):
            raise ValueError(f"str expected, got {type(value)}")
        return isodate.parse_duration(value)


class TableSpec(ShapeSpec):
    columns: ColumnsSpec | None
    header_first_cell: str = "Country"


class SlideMetadata(BaseModel):
    charts: dict[ChartName, ChartSpec] = Field(default_factory=dict)
    tables: dict[TableLocation, TableSpec] = Field(default_factory=dict)

    def find_fetchable_series_ids(self) -> set[SeriesId]:
        series_ids = set()
        for chart_spec in self.charts.values():
            series_ids |= set(chart_spec.find_fetchable_series_ids())
        for table_spec in self.tables.values():
            series_ids |= set(table_spec.find_fetchable_series_ids())
        return series_ids


class PresentationMetadata(BaseModel):
    slides: dict[str, SlideMetadata]

    def find_fetchable_series_ids(self) -> set[SeriesId]:
        result = set()
        for slide in self.slides.values():
            result |= slide.find_fetchable_series_ids()
        return result
