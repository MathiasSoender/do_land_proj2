import requests
import json

# A method which could be on a scheduler (Fetch from Matter, create/update metrics)
def upload_all_metrics():
    header = {"Content-type": "application/json"}
    with open('documentation/metrics.json') as f:
        metric_objs = json.load(f)

    createdAt = metric_objs["created"]

    for metric_obj in metric_objs["metrics"]:
        # Check existence
        if requests.get(f"http://127.0.0.1:5000/metric/{metric_obj['metric_id']}").status_code == 200:
            continue
        
        metric_obj["updated"] = createdAt
        res = requests.post("http://127.0.0.1:5000/metric", data = json.dumps(metric_obj), headers=header, verify=False)
        print(res)



if __name__ == "__main__":
    upload_all_metrics()


