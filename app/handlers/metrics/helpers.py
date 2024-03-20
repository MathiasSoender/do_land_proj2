from utils.db_utils import mongo
from models.metrics_entity import MetricEntity


def get_all_metrics_dict():
    cursor = mongo.db.metrics.find({})
    all_metrics = dict()
    for document in cursor:
        metric = MetricEntity(**document)
        if metric.metric_id in all_metrics:
            continue
        all_metrics[metric.metric_id] = metric
    return all_metrics
