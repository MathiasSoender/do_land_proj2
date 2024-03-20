# metric_id has also been added as index for fast retrievals.
import datetime
class MetricEntity:

    def __init__(
        self,
        metric_id,
        metric_name,
        metric_unit,
        metric_type,
        metric_equation,
        updated=None,
        _id="",
    ) -> None:
        self.metric_id = metric_id
        self.metric_name = metric_name
        self.metric_unit = metric_unit
        self.metric_type = metric_type
        self.metric_equation = metric_equation
        self._id = str(_id)
        self.updated = updated if updated is not None else datetime.datetime.now()
        # Keep this for future => re-runs of updating metrics.

    def to_dict(self):
        excluded = ['_id'] # Append with properties that should not be exported.
        return {
            key:value for key, value in self.__dict__.items() if key not in excluded
        }
