# Stop app container
docker ps --filter status=running --filter name=cc-api-main -q | xargs docker stop

# Delete app container
docker ps --filter status=exited --filter name=cc-api-main -q | xargs docker rm

# Delete app image
docker image rm cc-api --force

# Build image
docker build -t cc-api:0.0.1 .

# Start it up
docker run -p "127.0.0.1:5000:5000" --name "cc-api-main" -d