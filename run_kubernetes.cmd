
rem # This tags and uploads an image to Docker Hub

rem # Step 1:
rem # This is your Docker ID/path
rem # dockerpath=<>
set dockerpath=erarik/sentimentanalysis:latest
set deployment=deployment/my-sentimentanalysis


rem # Step 2
rem # Run the Docker Hub container with kubernetes
kubectl run my-sentimentanalysis --image=%dockerpath% --port 8000

rem # Step 3:
rem # List kubernetes pods
kubectl get pods

rem # Step 4:
rem # Forward the container port to a host
kubectl port-forward %deployment% 8000:80
