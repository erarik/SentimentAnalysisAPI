
set PORT=8000
echo "Port: %PORT%"

rem # POST method predict
curl -d @json.txt -H "Content-Type: application/json" -X POST http://localhost:%PORT%/predict