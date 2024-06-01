# Stop app container
sudo docker ps --filter status=running --filter name=cc-api-main -q | xargs docker stop

# Delete app container
sudo docker ps --filter status=exited --filter name=cc-api-main -q | xargs docker rm

# Delete app image
sudo docker image rm cc-api --force

# Build image
sudo docker build -t cc-api:0.0.1 .

# Start it up
sudo docker run -p "127.0.0.1:5000:5000" --name "cc-api-main" -d cc-api:0.0.1
