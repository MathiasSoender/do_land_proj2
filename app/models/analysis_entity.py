class AnalysisEntity:

    def __init__(
        self,
        created,
        external_id,
        holdings_matched,
        analysis,
        status="DONE",
        _id="",
        time_stamp=None,
    ):
        self.created = created
        self.external_id = external_id
        self.holdings_matched = holdings_matched
        self.analysis = analysis
        self.status = status
        self._id = str(_id)

    def reduce_analysis(self):
        if self.analysis is None:
            return
        # Dont waste storage on coverage == metric_value == 0.
        new_basics = [
            basic
            for basic in self.analysis["basic"]
            if float(basic["metric_value"]["raw"]) != 0.0
            and float(basic["coverage"]["weight"]) != 0.0
        ]

        # Dont waste storage on unused attrs (we can join in app layer)
        wanted_attrs = ["metric_id", "metric_value", "coverage", "metric_type"]
        new_basics = [{k: basic[k] for k in wanted_attrs} for basic in new_basics]

        self.analysis = {"basic": new_basics}

    # Placeholder document, for denoting failed creations
    def analysis_failed_placeholder(external_id):
        return AnalysisEntity(
            created=None,
            external_id=external_id,
            holdings_matched=None,
            analysis=None,
            status="FAILED",
        )

    def to_dict(self, exclude=[]):
        excluded = ["_id"] + exclude
        return {
            key: value for key, value in self.__dict__.items() if key not in excluded
        }

    def join_with_metrics(self, all_metrics_dict):
        for basic in self.analysis["basic"]:
            matched_basic = all_metrics_dict.get(basic["metric_id"])
            basic["metric_name"] = matched_basic.metric_name
            basic["metric_unit"] = matched_basic.metric_unit

    def get_metric_type_sum(self, metric_type):
        return sum(
            float(basic["metric_value"]["raw"])
            for basic in self.analysis["basic"]
            if basic["metric_type"] == metric_type
        )

    def get_metric_type_count(self, metric_type):
        return sum(
            float(basic["coverage"]["entity_count"])
            for basic in self.analysis["basic"]
            if basic["metric_type"] == metric_type
        )

    def get_metric_type_sum_and_count(self, metric_type):
        metric_val_raw = 0
        coverage_entity_count = 0
        for basic in self.analysis["basic"]:
            if basic["metric_type"] == metric_type:
                metric_val_raw += float(basic["metric_value"]["raw"])
                coverage_entity_count += float(basic["coverage"]["entity_count"])

        return metric_val_raw, coverage_entity_count
