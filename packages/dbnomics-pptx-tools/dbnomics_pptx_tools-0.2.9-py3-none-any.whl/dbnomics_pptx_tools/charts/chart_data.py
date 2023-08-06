from datetime import datetime
from typing import cast

import daiquiri
import numpy as np
from pandas import DataFrame, DatetimeIndex
from pptx.chart.data import CategoryChartData

from dbnomics_pptx_tools.metadata import ChartSpec

logger = daiquiri.getLogger(__name__)


def build_category_chart_data(chart_spec: ChartSpec, *, pivoted_df: DataFrame) -> CategoryChartData:
    chart_data = CategoryChartData()

    chart_data.categories = cast(DatetimeIndex, pivoted_df.index).to_pydatetime()

    for series_spec in chart_spec.series:
        series_id = series_spec.id
        if series_id not in pivoted_df:
            logger.warning("Could not find series %r among downloaded DBnomics series, ignoring", series_id)
            continue
        series = pivoted_df[series_id]
        series = series.replace({np.NaN: None})
        chart_data.add_series(series_spec.name, series.values)

    return chart_data


def filter_df_to_domain(df: DataFrame, *, max_datetime: datetime | None, min_datetime: datetime | None) -> DataFrame:
    if min_datetime is not None:
        df = df.query("period >= @min_datetime")
    if max_datetime is not None:
        df = df.query("period <= @max_datetime")
    return df
