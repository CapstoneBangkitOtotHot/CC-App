# Update codebase
git pull
git submodule update --init --recursive
git submodule update --remote

# Stop app container
sudo docker ps --filter status=running --filter name=cc-api-main -q | xargs sudo docker stop

# Delete app container
sudo docker ps --filter status=exited --filter name=cc-api-main -q | xargs sudo docker rm

# Delete app image
sudo docker image rm cc-api --force

# Build image
sudo docker build -t cc-api:0.0.1 .

# Start it up
sudo docker run --rm -p "127.0.0.1:5000:5000" --name "cc-api-main" -d cc-api:0.0.1
