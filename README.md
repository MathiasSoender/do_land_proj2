docker build -t do-land -f ./docker/Dockerfile.dev .
docker create --name do-land-container -p 80:80 do-land
docker start do-land-container