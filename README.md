## TODO LIST
Write swagger file


Add documentation (choices of datamapping)


Maybe add some more random/fun features



## Docker commands
Run everything from root (the dir where this file is, readme.md). These should build the image, create and launch container.



```
docker build -t do-land -f ./docker/Dockerfile.dev .
```


```
docker create --name do-land-container -p 80:80 do-land
```


```
docker start do-land-container
```
