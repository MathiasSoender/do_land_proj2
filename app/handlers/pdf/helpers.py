import pandas as pd
from handlers.analysis.analysis_handlers import (
    get_analysis_metric_types,
    get_analysis_metric_type_coverage_count,
    get_analysis_metric_type_raw_sum,
)


def generate_df_for_pdf(analysis_id) -> pd.DataFrame:
    metric_types_used = get_analysis_metric_types(analysis_id)
    metric_sums = ["_METRIC_SUMS_"]
    metric_occurences = ["_METRIC_OCCURENCES_"]

    for metric_type in metric_types_used:
        metric_raw_sum = get_analysis_metric_type_raw_sum(analysis_id, metric_type)
        metric_occurence = get_analysis_metric_type_coverage_count(analysis_id, metric_type)
        metric_sums.append(round(metric_raw_sum, 2))
        metric_occurences.append(metric_occurence)

    metric_types_used = ["_METRIC_TYPE_"] + metric_types_used
    data = {
        "Metric_Type": metric_types_used,
        "metric_sum": metric_sums,
        "metric_occurences": metric_occurences,
    }

    return pd.DataFrame(data)
