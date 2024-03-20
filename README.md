# DoLand x Matter microservice
The purpose of this microservice is to provide a data handler between Matter and Doland.

## Build commands

### Debug
Debug run.py to start the backend locally. It should be available on localhost:80.

### Docker commands
Run everything from root (the dir where this file is, readme.md). These should build the image, create and launch container. Run the commands in a shell. It requires Docker to be installed on your system (see Docker Desktop).


```
docker build -t do-land -f ./docker/Dockerfile.dev .
```


```
docker create --name do-land-container -p 80:80 do-land
```


```
docker start do-land-container
```

Again, the backend is available on localhost:80. Do not try to run the docker container and debug locally at the same time - this wont work.


### Endpoint details
1. GET / : Retreives a list of all analysis created, with full information. An analysis which have just been created will probably not show (async, it takes around 2s for an analysis to be created from a portfolio)

2. POST / : Must be same format as explained in Matter API. Returns an ID which corresponds to the analysis created from the posted portfolio. This ID corresponds to the {analysis_id} below.

3. GET /{analysis_id} : Must use above returned ID as analysis_id. This returns the metrics which have metric_value.raw > 0 or coverage.entity_count > 0. See below note.

4. GET /{analysis_id}/{metric_type} : Returns the sum of metric_value.raw for the given metric_type, and the count is computed and returned by summing over coverage.entity_count. 

5. GET /pdf/{analysis_id} : Returns the PDF built on information from 3. and 4.

*Important*: Metrics of an analysis are NOT saved if metric_value.raw is 0 AND coverage.entity_count is 0. Why? I saw that each analysis contains all metrics (988 to date). That is also why I look in the coverage.entity_count for computing "the count of objects associated with the specified metric type", as this is my best understanding at the given time.
 
 There are also 2 other endpoints
 1. POST /metric : Create a metric in the database.
 2. GET /metric/{metric_id} : Gets a metric with specific metrid_id.
 3. /swagger : Swagger documentation.

### Future work

1. Keep the Metrics database synced with Matter (scheduler).
2. More error handling (repeated ISIN? bad ISIN? Why did an analysis fail?)
3. PDF Beautify
4. Deployment (Works on my machine!)