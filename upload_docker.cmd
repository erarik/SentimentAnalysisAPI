rem # This file tags and uploads an image to Docker Hub

rem # Assumes that an image is built via `run_docker.sh`

rem # Step 1:
rem # Create dockerpath
rem # dockerpath=<your docker ID/path>
set dockerpath=erarik/sentimentanalysis
set tag=sentimentanalysis

rem # Step 2:  
rem # Authenticate & tag
echo "Docker ID and Image: $dockerpath"
docker login --username=erarik
docker tag %tag% %dockerpath%:latest

rem # Step 3:
rem # Push image to a docker repository
docker push %dockerpath%
