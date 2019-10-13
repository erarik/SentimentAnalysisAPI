
rem ## Complete the following steps to get Docker running locally

rem # Step 1:
rem # Build image and add a descriptive tag
docker build --tag=sentimentanalysis .

rem # Step 2: 
rem # List docker images
docker image ls

rem # Step 3: 
rem # Run flask app
docker run -p 8000:80 sentimentanalysis
