

if __name__ == "__main__":
    import json
    with open('analysis.json') as f:
        json_obj = json.load(f)
        print(json_obj)

