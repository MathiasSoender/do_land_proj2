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

2. POST / : Must be same format as explained in Matter API. Returns an ID which corresponds to the analysis created from the posted portfolio.

3. GET /{analysis_id} : Must use above returned ID as analysis_id.

4. GET /{analysis_id}/{metric_type} : Returns the sum of raw values, and the count is returned by coverage.entity_count (summed)


Important: Metrics of an analysis are NOT saved if raw weight is 0 AND coverage.entity_count is 0!
 